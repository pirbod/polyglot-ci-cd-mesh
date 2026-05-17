# 10-Minute Demo Script

## Setup

```bash
make install
make test
make demo
```

Open http://localhost:5173.

## Talk Track

1. Executive Overview: show mesh health, build success, readiness, API gate status, supply-chain risk, and AKS/EKS/GKE health.
2. Polyglot Pipelines: click `Run` on Python service, then show the new run in history.
3. Multi-Cloud Delivery: click `Promote to prod` and explain local promotion mirrors the controlled production path.
4. API Security Gate: click `Compliant`, then `Non-compliant`. Show findings, risk score, and remediation.
5. Supply Chain: explain SBOM, container scan, dependency scan, attestation, image signing, failing dependency, and remediation path.
6. GitOps View: find the out-of-sync app and click `Rollback`.
7. Evidence Center: download `openapi-gate-fail.json`, `sbom-report.json`, and `scan-report.json`.
8. Close with Terraform, Helm, ArgoCD, and OIDC production path.

## What Each Page Proves

| Page | Proof |
| --- | --- |
| Overview | Stakeholder-ready health and risk posture. |
| Pipelines | Runtime-aware delivery for Java, .NET, Node.js, and Python. |
| Cloud | AKS, EKS, and GKE architecture without local cloud spend. |
| API Gate | Real pass/fail security logic, not a placeholder. |
| Supply Chain | Evidence-first SBOM, scan, signing, and attestation story. |
| GitOps | Apps-of-apps topology and rollback behavior. |
| Evidence | Downloadable proof artifacts for review. |
