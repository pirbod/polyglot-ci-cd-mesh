from pathlib import Path
import json
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]


class EvidenceTests(unittest.TestCase):
    def test_evidence_reports_are_generated(self):
        subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_demo_data.py")], check=True)
        expected = [
            "demo-state.json",
            "test-report.json",
            "openapi-gate-pass.json",
            "openapi-gate-fail.json",
            "sbom-report.json",
            "scan-report.json",
            "terraform-validation-result.json",
            "security-evidence.json",
        ]
        missing = [name for name in expected if not (ROOT / "evidence" / name).exists()]
        self.assertEqual(missing, [])
        gate = json.loads((ROOT / "evidence" / "openapi-gate-fail.json").read_text(encoding="utf-8"))
        self.assertEqual(gate["status"], "fail")

    def test_screenshot_assets_are_generated(self):
        subprocess.run([sys.executable, str(ROOT / "scripts" / "capture_screenshots.py")], check=True)
        screenshots = list((ROOT / "docs" / "screenshots").glob("*.svg"))
        self.assertGreaterEqual(len(screenshots), 8)


if __name__ == "__main__":
    unittest.main()
