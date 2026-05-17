from __future__ import annotations

from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT / "dashboard" / "backend"
GATE_DIR = ROOT / "security-gates" / "api-policy-gate"
for item in (BACKEND_DIR, GATE_DIR):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from data import EVIDENCE_DIR, default_state, save_state  # noqa: E402
from policy_gate import validate_file  # noqa: E402


def write_json(name: str, payload: dict | list, overwrite: bool = True) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    target = EVIDENCE_DIR / name
    if target.exists() and not overwrite:
        return
    target.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    state = default_state()
    save_state(state)
    compliant = validate_file(ROOT / "security-gates" / "openapi-rules" / "compliant-api.yaml")
    failing = validate_file(ROOT / "security-gates" / "openapi-rules" / "non-compliant-api.yaml")
    write_json(
        "test-report.json",
        {"status": "not-run", "suites": ["policy", "dashboard-api", "repo-contract"], "generated_by": "local"},
        overwrite=False,
    )
    write_json("openapi-gate-pass.json", compliant)
    write_json("openapi-gate-fail.json", failing)
    write_json(
        "sbom-report.json",
        {
            "status": "generated",
            "format": "CycloneDX-compatible demo summary",
            "components": [
                {"name": "java-service", "runtime": "java", "risk": "low"},
                {"name": "dotnet-service", "runtime": "dotnet", "risk": "low"},
                {"name": "node-service", "runtime": "node", "risk": "medium"},
                {"name": "python-service", "runtime": "python", "risk": "low"},
            ],
        },
    )
    write_json(
        "scan-report.json",
        {
            "status": "warn",
            "critical": 0,
            "high": 1,
            "medium": 5,
            "failing_service": "node-service",
            "remediation": "Upgrade demo-transitive-package to the patched version.",
        },
    )
    write_json(
        "terraform-validation-result.json",
        {
            "status": "ready",
            "mode": "local validation",
            "modules": ["cluster-aks", "cluster-eks", "cluster-gke", "registry", "observability"],
        },
    )
    write_json(
        "security-evidence.json",
        {
            "oidc": "documented",
            "least_privilege": "workflow permissions are scoped",
            "api_gate": compliant["status"],
            "attestation": "simulated locally, real path documented for release workflow",
            "image_signing": "simulated locally, real path documented for release workflow",
        },
    )
    print(f"Generated demo evidence in {EVIDENCE_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
