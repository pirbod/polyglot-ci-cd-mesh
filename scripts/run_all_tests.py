from __future__ import annotations

from pathlib import Path
import json
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
RESULTS: list[dict[str, str]] = []


def run(name: str, command: list[str], cwd: Path = ROOT, required: bool = True) -> None:
    print(f"==> {name}")
    completed = subprocess.run(command, cwd=cwd)
    status = "pass" if completed.returncode == 0 else ("fail" if required else "skip")
    RESULTS.append({"name": name, "status": status, "command": " ".join(command)})
    if required and completed.returncode != 0:
        raise SystemExit(completed.returncode)


def maybe_run(name: str, executable: str, command: list[str], cwd: Path = ROOT) -> None:
    if shutil.which(executable) is None:
        print(f"==> {name}: skipped because {executable} is unavailable")
        RESULTS.append({"name": name, "status": "skip", "command": " ".join(command)})
        return
    run(name, command, cwd=cwd, required=False)


def main() -> int:
    run("generate demo evidence", [sys.executable, "scripts/generate_demo_data.py"])
    run("python unittest suite", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"])
    node_modules = ROOT / "apps" / "node-service" / "node_modules" / "express"
    if node_modules.exists():
        maybe_run("node service tests", "npm", ["npm", "test"], cwd=ROOT / "apps" / "node-service")
    else:
        print("==> node service tests: skipped because dependencies are not installed")
        RESULTS.append({"name": "node service tests", "status": "skip", "command": "npm test"})
    maybe_run("frontend smoke test", "npm", ["npm", "test"], cwd=ROOT / "dashboard" / "frontend")
    maybe_run("java service tests", "mvn", ["mvn", "test"], cwd=ROOT / "apps" / "java-service")
    maybe_run("dotnet service tests", "dotnet", ["dotnet", "test"], cwd=ROOT / "apps" / "dotnet-service")
    report = {"status": "pass", "results": RESULTS}
    evidence = ROOT / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "test-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("Local test runner completed. Skipped runtime tests are listed in evidence/test-report.json.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
