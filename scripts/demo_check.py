from __future__ import annotations

from pathlib import Path
import json
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_demo_data.py")], check=True)
    state_path = ROOT / "evidence" / "demo-state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    required = ["overview", "pipelines", "clouds", "api_gate", "supply_chain", "gitops"]
    missing = [name for name in required if name not in state]
    if missing:
        print(f"Missing demo sections: {', '.join(missing)}")
        return 1
    print("Demo check passed: local state and evidence are available.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
