from __future__ import annotations

from pathlib import Path
import json
import sys


ROOT = Path(__file__).resolve().parents[1]
GATE_DIR = ROOT / "security-gates" / "api-policy-gate"
sys.path.insert(0, str(GATE_DIR))

from policy_gate import validate_file  # noqa: E402


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: validate_openapi.py <spec> [output.json]")
        return 2
    result = validate_file(sys.argv[1])
    encoded = json.dumps(result, indent=2)
    if len(sys.argv) > 2:
        output = Path(sys.argv[2])
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
