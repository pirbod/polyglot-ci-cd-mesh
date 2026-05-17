from __future__ import annotations

from pathlib import Path
import os
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_demo_data.py")], check=True)
    uvicorn = shutil.which("uvicorn") or str(ROOT / ".venv" / "bin" / "uvicorn")
    npm = shutil.which("npm")
    if not Path(uvicorn).exists() and shutil.which("uvicorn") is None:
        docker = shutil.which("docker")
        if docker is None:
            print("FastAPI dependencies are missing and Docker is unavailable. Run `make install`, then rerun `make demo`.")
            return 1
        print("FastAPI host dependencies are missing; starting the Docker Compose demo path.")
        return subprocess.call([docker, "compose", "up", "--build"], cwd=ROOT)
    if npm is None:
        print("Node.js npm is missing. Install Node.js 20+, then rerun `make demo`.")
        return 1
    env = os.environ.copy()
    env.setdefault("DASHBOARD_API_URL", "http://localhost:8080")
    backend = subprocess.Popen(
        [uvicorn, "app:app", "--host", "0.0.0.0", "--port", env.get("DASHBOARD_API_PORT", "8080")],
        cwd=ROOT / "dashboard" / "backend",
        env=env,
    )
    try:
        print("Dashboard API: http://localhost:8080")
        print("Dashboard UI:  http://localhost:5173")
        subprocess.run(["npm", "run", "dev", "--", "--host", "0.0.0.0"], cwd=ROOT / "dashboard" / "frontend", env=env, check=True)
    finally:
        backend.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
