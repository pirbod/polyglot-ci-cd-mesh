from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import json

import yaml


HTTP_METHODS = {"get", "put", "post", "delete", "patch", "options", "head", "trace"}
PUBLIC_MARKERS = ("x-public", "x-public-endpoint")


@dataclass
class Finding:
    code: str
    severity: str
    message: str
    remediation: str
    location: str


def _load_spec(raw: str | bytes | dict[str, Any]) -> dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw
    try:
        parsed = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ValueError(f"OpenAPI could not be parsed: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("OpenAPI document must be a mapping")
    return parsed


def _is_public(operation: dict[str, Any]) -> bool:
    return any(operation.get(marker) is True for marker in PUBLIC_MARKERS)


def _operation_security(spec: dict[str, Any], operation: dict[str, Any]) -> Any:
    if "security" in operation:
        return operation.get("security")
    return spec.get("security")


def _has_auth_scheme(spec: dict[str, Any]) -> bool:
    schemes = spec.get("components", {}).get("securitySchemes", {})
    if not isinstance(schemes, dict):
        return False
    accepted = {"apiKey", "http", "oauth2", "openIdConnect"}
    return any(isinstance(value, dict) and value.get("type") in accepted for value in schemes.values())


def _has_rate_limit(spec: dict[str, Any], operation: dict[str, Any] | None = None) -> bool:
    operation = operation or {}
    return any(
        key in spec or key in operation
        for key in ("x-rate-limit", "x-tyk-rate-limit", "x-tyk-quota", "x-gateway-rate-limit")
    )


def _has_policy_mapping(spec: dict[str, Any], operation: dict[str, Any] | None = None) -> bool:
    operation = operation or {}
    return any(key in spec or key in operation for key in ("x-tyk-policy-id", "x-tyk-policy", "x-api-policy"))


def validate_openapi(raw: str | bytes | dict[str, Any]) -> dict[str, Any]:
    findings: list[Finding] = []
    try:
        spec = _load_spec(raw)
    except ValueError as exc:
        finding = Finding(
            code="parse_error",
            severity="critical",
            message=str(exc),
            remediation="Provide a valid OpenAPI JSON or YAML document.",
            location="$",
        )
        return _result([finding], {"parseable": False})

    evidence: dict[str, Any] = {
        "parseable": True,
        "openapi": spec.get("openapi"),
        "title": spec.get("info", {}).get("title"),
        "version": spec.get("info", {}).get("version"),
        "operation_count": 0,
        "public_operations": 0,
        "auth_scheme_present": _has_auth_scheme(spec),
        "rate_limit_present": _has_rate_limit(spec),
        "tyk_policy_present": _has_policy_mapping(spec),
    }

    if not spec.get("openapi"):
        findings.append(
            Finding(
                "missing_openapi_version",
                "high",
                "OpenAPI version is missing.",
                "Add an openapi field such as 3.0.3 or 3.1.0.",
                "$.openapi",
            )
        )

    paths = spec.get("paths")
    if not isinstance(paths, dict) or not paths:
        findings.append(
            Finding(
                "missing_paths",
                "critical",
                "No API paths are defined.",
                "Define at least one path with operations.",
                "$.paths",
            )
        )
        return _result(findings, evidence)

    if not evidence["auth_scheme_present"]:
        findings.append(
            Finding(
                "missing_auth_scheme",
                "critical",
                "No supported auth scheme is defined.",
                "Add components.securitySchemes with apiKey, http, oauth2, or openIdConnect.",
                "$.components.securitySchemes",
            )
        )

    if not evidence["rate_limit_present"]:
        findings.append(
            Finding(
                "missing_rate_limit",
                "high",
                "No gateway rate-limit extension is defined.",
                "Add x-tyk-rate-limit or x-rate-limit with burst and sustained limits.",
                "$",
            )
        )

    if not evidence["tyk_policy_present"]:
        findings.append(
            Finding(
                "missing_tyk_policy_mapping",
                "high",
                "No Tyk policy mapping is defined.",
                "Add x-tyk-policy-id or x-tyk-policy to bind the API to a managed gateway policy.",
                "$",
            )
        )

    required_metadata = spec.get("x-service-metadata", {})
    for key in ("owner", "runtime", "criticality"):
        if not required_metadata.get(key):
            findings.append(
                Finding(
                    f"missing_service_{key}",
                    "medium",
                    f"Service metadata is missing {key}.",
                    "Add x-service-metadata with owner, runtime, and criticality.",
                    "$.x-service-metadata",
                )
            )

    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            evidence["operation_count"] += 1
            location = f"$.paths.{path}.{method}"
            public = _is_public(operation)
            if public:
                evidence["public_operations"] += 1
            security = _operation_security(spec, operation)
            if not public and not security:
                findings.append(
                    Finding(
                        "operation_missing_security",
                        "critical",
                        f"{method.upper()} {path} does not require auth.",
                        "Add an operation security requirement or explicitly mark a safe public endpoint.",
                        location,
                    )
                )
            if "admin" in path.lower() and (public or not security):
                findings.append(
                    Finding(
                        "public_admin_endpoint",
                        "critical",
                        f"{method.upper()} {path} exposes an admin-like path without auth.",
                        "Require auth for admin paths and avoid public wildcard admin endpoints.",
                        location,
                    )
                )
            if "*" in path and public:
                findings.append(
                    Finding(
                        "wildcard_public_path",
                        "critical",
                        f"{method.upper()} {path} marks a wildcard path public.",
                        "Replace wildcard public paths with explicit, authenticated operations.",
                        location,
                    )
                )
            if not operation.get("operationId"):
                findings.append(
                    Finding(
                        "missing_operation_id",
                        "medium",
                        f"{method.upper()} {path} is missing operationId.",
                        "Add a stable operationId for traceability, gateway policy, and audit evidence.",
                        location,
                    )
                )
            if not operation.get("tags"):
                findings.append(
                    Finding(
                        "missing_tags",
                        "low",
                        f"{method.upper()} {path} is missing tags.",
                        "Add at least one tag for ownership and catalog grouping.",
                        location,
                    )
                )

    return _result(findings, evidence)


def _result(findings: list[Finding], evidence: dict[str, Any]) -> dict[str, Any]:
    weights = {"critical": 30, "high": 18, "medium": 8, "low": 3}
    risk_score = min(100, sum(weights.get(finding.severity, 1) for finding in findings))
    status = "pass" if risk_score == 0 else "fail"
    return {
        "status": status,
        "risk_score": risk_score,
        "findings": [asdict(finding) for finding in findings],
        "remediation": [finding.remediation for finding in findings],
        "policy_evidence": evidence,
    }


def validate_file(path: str | Path) -> dict[str, Any]:
    return validate_openapi(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Validate OpenAPI security posture")
    parser.add_argument("spec", help="OpenAPI JSON or YAML file")
    parser.add_argument("--output", help="Optional JSON output path")
    args = parser.parse_args()

    result = validate_file(args.spec)
    encoded = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
