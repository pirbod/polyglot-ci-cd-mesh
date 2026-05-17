# Threat Model

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Long-lived cloud secrets | Credential theft can lead to cloud compromise. | Use OIDC federation, short-lived tokens, scoped roles, and protected environments. |
| Malicious pull requests | A PR can attempt to exfiltrate secrets or weaken policy. | Keep PR workflow permissions minimal, avoid secrets on untrusted PRs, and require review. |
| Compromised dependency | Runtime dependency can introduce vulnerable code. | Run dependency review, OSV, SBOM generation, and runtime-specific tests. |
| Insecure OpenAPI changes | Public or unauthenticated sensitive endpoints can ship. | Enforce the API policy gate and OPA rules before merge. |
| Drift between Git and cluster | Manual cluster changes bypass review. | Use ArgoCD sync, health checks, rollback, and drift visibility. |
| Vulnerable container image | Known CVEs can reach deployment. | Scan filesystem and images, block critical findings, and record remediation. |
| Overprivileged cloud identity | Deployment automation can exceed intended blast radius. | Use separate roles per environment, least privilege, approval gates, and audit logs. |

## Residual Risk

The local demo simulates cloud state. A production rollout must validate provider-specific IAM, network policy, registry access, and cluster admission controls before handling real workloads.
