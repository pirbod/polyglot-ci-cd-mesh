from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "security-gates" / "api-policy-gate"))

from policy_gate import validate_file  # noqa: E402


class OpenApiGateTests(unittest.TestCase):
    def test_compliant_spec_passes(self):
        result = validate_file(ROOT / "security-gates" / "openapi-rules" / "compliant-api.yaml")
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["risk_score"], 0)

    def test_non_compliant_spec_fails(self):
        result = validate_file(ROOT / "security-gates" / "openapi-rules" / "non-compliant-api.yaml")
        self.assertEqual(result["status"], "fail")
        self.assertGreater(result["risk_score"], 0)
        codes = {finding["code"] for finding in result["findings"]}
        self.assertIn("missing_auth_scheme", codes)
        self.assertIn("public_admin_endpoint", codes)


if __name__ == "__main__":
    unittest.main()
