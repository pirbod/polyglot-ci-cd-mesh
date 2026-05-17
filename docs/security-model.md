# Security Model

The security model combines least-privilege automation, API policy-as-code, supply-chain evidence, and GitOps drift control.

## Controls

- GitHub Actions permissions are scoped per workflow.
- Cloud authentication is OIDC-based in the production path.
- OpenAPI changes are validated by a local Python policy gate.
- OPA policies express portable API rules for auth, admin exposure, rate limits, and metadata.
- SBOM, scan, attestation, and signing evidence are generated or simulated locally.
- ArgoCD keeps cluster state aligned with Git.

## OIDC

Production deploy jobs should use:

- AWS: IAM role trust policy for GitHub OIDC subject claims.
- Azure: federated identity credential bound to a deployment service principal.
- GCP: Workload Identity Federation mapped to a deployment service account.

Long-lived cloud keys are not required for the default demo and should not be stored in repository secrets.

## Least Privilege

Recommended workflow permissions:

- CI: `contents: read`.
- Security: `contents: read`, `security-events: write`, `id-token: write`, `attestations: write`.
- Release: `contents: read`, `packages: write`, `id-token: write`, `attestations: write`.
- Terraform validation: `contents: read`.

Production environments should require human approval, branch protection, and separate roles for plan and apply.

## Supply Chain

The local path writes deterministic evidence files so the dashboard can prove the control surface. The production path should use Syft or an equivalent SBOM tool, Trivy or equivalent scanning, GitHub provenance attestations, and keyless image signing.
