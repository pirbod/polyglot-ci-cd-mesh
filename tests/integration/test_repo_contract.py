from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]


class RepositoryContractTests(unittest.TestCase):
    def test_required_files_exist(self):
        required = [
            "README.md",
            "Makefile",
            "docker-compose.yml",
            "apps/java-service/openapi.yaml",
            "apps/dotnet-service/openapi.yaml",
            "apps/node-service/openapi.yaml",
            "apps/python-service/openapi.yaml",
            "dashboard/backend/app.py",
            "dashboard/frontend/src/App.tsx",
            "security-gates/api-policy-gate/policy_gate.py",
            "terraform/main.tf",
            "argo-cd/root-app.yaml",
            "charts/polyglot-service/Chart.yaml",
        ]
        missing = [item for item in required if not (ROOT / item).exists()]
        self.assertEqual(missing, [])

    def test_docker_compose_health_surfaces(self):
        compose = yaml.safe_load((ROOT / "docker-compose.yml").read_text(encoding="utf-8"))
        services = compose["services"]
        for service in [
            "dashboard-api",
            "dashboard-web",
            "api-policy-gate",
            "java-service",
            "dotnet-service",
            "node-service",
            "python-service",
        ]:
            self.assertIn(service, services)
            self.assertIn("ports", services[service])

    def test_workflows_are_split_by_responsibility(self):
        workflows = {path.name for path in (ROOT / ".github" / "workflows").glob("*.yml")}
        self.assertEqual({"ci.yml", "security.yml", "terraform-validate.yml", "release.yml"}, workflows)


if __name__ == "__main__":
    unittest.main()
