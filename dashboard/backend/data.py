from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json
import random
import sys


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_DIR = ROOT / "evidence"
STATE_FILE = EVIDENCE_DIR / "demo-state.json"
GATE_DIR = ROOT / "security-gates" / "api-policy-gate"
if str(GATE_DIR) not in sys.path:
    sys.path.insert(0, str(GATE_DIR))

from policy_gate import validate_file  # noqa: E402


RUNTIMES = {
    "java": {"name": "Java service", "runtime": "Java", "path": "apps/java-service", "risk": 12},
    "dotnet": { "name": ".NET service", "runtime": ".NET", "path": "apps/dotnet-service", "risk": 18},
    "node": {"name": "Node.js service", "runtime": "Node.js", "path": "apps/node-service", "risk": 42},
    "python": {"name": "Python service", "runtime": "Python", "path": "apps/python-service", "risk": 8},
}

CLOUD_TARGETS = {
    "aks": {"name": "AKS", "region": "westeurope", "cluster": "mesh-aks-dev"},
    "eks": {"name": "EKS", "region": "eu-central-1", "cluster": "mesh-eks-dev"},
    "gke": {"name": "GKE", "region": "europe-west3", "cluster": "mesh-gke-dev"},
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def default_state() -> dict[str, Any]:
    pipelines = []
    for key, service in RUNTIMES.items():
        pipelines.append(
            {
                "id": key,
                "service": service["name"],
                "runtime": service["runtime"],
                "build": "pass",
                "tests": "pass",
                "scan": "warn" if key == "node" else "pass",
                "image": "built",
                "sbom": "generated",
                "attestation": "ready",
                "deploy_readiness": "blocked" if key == "node" else "ready",
                "risk_score": service["risk"],
                "last_run": now_iso(),
            }
        )
    clouds = []
    for key, cloud in CLOUD_TARGETS.items():
        clouds.append(
            {
                "id": key,
                "name": cloud["name"],
                "cluster": cloud["cluster"],
                "region": cloud["region"],
                "terraform_plan": "validated",
                "registry": "available",
                "argocd_sync": "synced",
                "health": "healthy",
                "environment": "dev",
            }
        )
    gitops = []
    revisions = {"java": "a1f8421", "dotnet": "c72b901", "node": "f8d9120", "python": "b51e7c3"}
    for service_id, service in RUNTIMES.items():
        for cloud_id, cloud in CLOUD_TARGETS.items():
            gitops.append(
                {
                    "id": f"{service_id}-{cloud_id}",
                    "service": service["name"],
                    "cluster": cloud["name"],
                    "sync": "OutOfSync" if service_id == "node" and cloud_id == "eks" else "Synced",
                    "health": "Progressing" if service_id == "node" and cloud_id == "eks" else "Healthy",
                    "revision": revisions[service_id],
                    "wave": 20 if service_id in {"node", "python"} else 10,
                }
            )
    return {
        "generated_at": now_iso(),
        "overview": {
            "mesh_health_score": 92,
            "build_success_rate": 97,
            "deployment_readiness": 88,
            "security_gate_status": "passing",
            "supply_chain_risk_score": 24,
        },
        "pipelines": pipelines,
        "pipeline_runs": [
            {"id": "run-1001", "service": "Python service", "status": "pass", "duration_seconds": 41, "created_at": now_iso()},
            {"id": "run-1000", "service": "Node.js service", "status": "warn", "duration_seconds": 56, "created_at": now_iso()},
        ],
        "clouds": clouds,
        "api_gate": {
            "selected": "compliant-api.yaml",
            "last_result": validate_file(ROOT / "security-gates" / "openapi-rules" / "compliant-api.yaml"),
        },
        "supply_chain": {
            "sbom": "generated",
            "container_scan": "0 critical, 1 high, 5 medium",
            "dependency_scan": "node-service has one simulated high-risk dependency",
            "attestation": "generated",
            "signed_images": "simulated signatures present",
            "failing_service": "Node.js service",
            "remediation": "Upgrade demo-transitive-package from 1.2.0 to 1.2.3 and rerun the scan.",
            "final_pass_state": "Python service and Java service are clean in the demo evidence set.",
        },
        "gitops": gitops,
    }


def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        save_state(default_state())
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def save_state(state: dict[str, Any]) -> None:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def run_pipeline(service_id: str) -> dict[str, Any]:
    state = load_state()
    if service_id not in RUNTIMES:
        raise KeyError(service_id)
    service = RUNTIMES[service_id]
    sequence = len(state.get("pipeline_runs", [])) + 1001
    random_seed = f"{service_id}-{sequence}"
    random.seed(random_seed)
    status = "warn" if service_id == "node" else "pass"
    duration = random.randint(32, 74)
    run = {
        "id": f"run-{sequence}",
        "service": service["name"],
        "status": status,
        "duration_seconds": duration,
        "created_at": now_iso(),
    }
    state["pipeline_runs"].insert(0, run)
    for pipeline in state["pipelines"]:
        if pipeline["id"] == service_id:
            pipeline["last_run"] = run["created_at"]
            pipeline["deploy_readiness"] = "blocked" if status == "warn" else "ready"
    save_state(state)
    return run


def promote(environment: str = "prod") -> dict[str, Any]:
    state = load_state()
    for cloud in state["clouds"]:
        cloud["environment"] = environment
        cloud["terraform_plan"] = "promotion simulated"
        cloud["argocd_sync"] = "synced"
    save_state(state)
    return {"status": "promoted", "environment": environment, "updated_at": now_iso()}


def rollback(app_id: str) -> dict[str, Any]:
    state = load_state()
    for app in state["gitops"]:
        if app["id"] == app_id:
            app["sync"] = "Synced"
            app["health"] = "Healthy"
            app["revision"] = "rollback-" + app["revision"][:7]
            save_state(state)
            return deepcopy(app)
    raise KeyError(app_id)


def list_evidence() -> list[dict[str, str]]:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    return [
        {
            "name": path.name,
            "path": str(path.relative_to(ROOT)),
            "type": "json" if path.suffix == ".json" else path.suffix.lstrip("."),
        }
        for path in sorted(EVIDENCE_DIR.glob("*"))
        if path.is_file()
    ]
