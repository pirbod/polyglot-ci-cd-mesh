from __future__ import annotations

from pathlib import Path
import json
import os
import sys


ROOT = Path(__file__).resolve().parents[1]
RESTRICTED = "co" + "dex"
SKIP_DIRS = {".git", ".venv", "node_modules", "dist", "build", "target", "obj", "__pycache__"}
REQUIRED_FILES = [
    "README.md",
    "Makefile",
    "docker-compose.yml",
    ".github/workflows/ci.yml",
    ".github/workflows/security.yml",
    ".github/workflows/release.yml",
    ".github/workflows/terraform-validate.yml",
    "apps/java-service/Dockerfile",
    "apps/dotnet-service/Dockerfile",
    "apps/node-service/Dockerfile",
    "apps/python-service/Dockerfile",
    "dashboard/backend/app.py",
    "dashboard/frontend/package.json",
    "security-gates/api-policy-gate/policy_gate.py",
    "terraform/README.md",
    "argo-cd/root-app.yaml",
    "charts/polyglot-service/Chart.yaml",
    "docs/architecture.md",
    "docs/demo-script.md",
    "docs/security-model.md",
    "docs/threat-model.md",
    "docs/local-demo.md",
    "docs/production-roadmap.md",
    "docs/scoring.md",
]


def project_files() -> list[Path]:
    files: list[Path] = []
    for current, dirs, names in os.walk(ROOT):
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
        base = Path(current)
        for name in names:
            files.append(base / name)
    return files


def main() -> int:
    errors: list[str] = []
    for item in REQUIRED_FILES:
        if not (ROOT / item).exists():
            errors.append(f"missing required file: {item}")
    for path in project_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if RESTRICTED in text.lower():
            errors.append(f"restricted term found in {path.relative_to(ROOT)}")
    result = {"status": "fail" if errors else "pass", "errors": errors}
    evidence = ROOT / "evidence"
    evidence.mkdir(exist_ok=True)
    (evidence / "repo-quality-report.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if errors:
        print("\n".join(errors))
        return 1
    print("Repository quality validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
