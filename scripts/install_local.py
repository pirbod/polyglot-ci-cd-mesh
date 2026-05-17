from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys
import venv


ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT / ".venv"


def run(command: list[str], cwd: Path = ROOT, required: bool = True, timeout: int | None = None) -> bool:
    print("+ " + " ".join(command))
    try:
        completed = subprocess.run(command, cwd=cwd, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f"Command timed out after {timeout} seconds.")
        if required:
            raise SystemExit(124)
        return False
    if completed.returncode != 0 and required:
        raise SystemExit(completed.returncode)
    return completed.returncode == 0


def python_install() -> None:
    try:
        if not VENV.exists():
            venv.EnvBuilder(with_pip=True).create(VENV)
        pip = VENV / "bin" / "pip"
        if pip.exists():
            run([str(pip), "install", "--upgrade", "pip"])
            run([str(pip), "install", "-r", "requirements-dev.txt"])
            return
    except Exception as exc:
        print(f"Python virtual environment unavailable: {exc}")

    if run([sys.executable, "-m", "pip", "--version"], required=False):
        run([sys.executable, "-m", "pip", "install", "--user", "-r", "requirements-dev.txt"])
        return

    print("Python package installer unavailable; local Python-only fallback tests can still run.")


def npm_install() -> None:
    npm = shutil.which("npm")
    if npm is None:
        print("npm unavailable; frontend and Node.js dependency install skipped.")
        return
    npm_args = ["install", "--fetch-retries=1", "--fetch-timeout=30000"]
    run([npm, *npm_args], cwd=ROOT / "dashboard" / "frontend", timeout=120)
    run([npm, *npm_args], cwd=ROOT / "apps" / "node-service", timeout=120)


def main() -> int:
    python_install()
    npm_install()
    print("Install step completed with available local tooling.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
