from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "dashboard" / "backend"))


class DashboardApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            from fastapi.testclient import TestClient
            from app import app
        except ImportError as exc:
            raise unittest.SkipTest(f"FastAPI test dependencies unavailable: {exc}") from exc
        cls.client = TestClient(app)

    def test_state_endpoint_has_core_sections(self):
        response = self.client.get("/api/state")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        for key in ["overview", "pipelines", "clouds", "api_gate", "supply_chain", "gitops", "evidence"]:
            self.assertIn(key, payload)

    def test_pipeline_run_is_recorded(self):
        before = self.client.get("/api/state").json()["pipeline_runs"]
        response = self.client.post("/api/pipelines/run", json={"service_id": "python"})
        self.assertEqual(response.status_code, 200)
        after = self.client.get("/api/state").json()["pipeline_runs"]
        self.assertEqual(len(after), len(before) + 1)

    def test_openapi_selection_returns_policy_result(self):
        response = self.client.post("/api/openapi/select", json={"filename": "non-compliant-api.yaml"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "fail")


if __name__ == "__main__":
    unittest.main()
