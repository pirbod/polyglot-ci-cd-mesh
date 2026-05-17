# Terraform Multi-Cloud Model

The default Terraform path is built for local validation. It models AKS, EKS, GKE, registry, and observability modules without creating paid cloud resources. This keeps the demo safe while preserving the same module boundaries used for a production rollout.

## Local Validation

```bash
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform fmt -check -recursive
terraform -chdir=terraform validate
```

## Production Path

Real deployments replace the local module internals with cloud resources and authenticate through GitHub Actions OIDC:

- AWS: AssumeRoleWithWebIdentity into a tightly scoped EKS provisioning role.
- Azure: federated identity credential mapped to a service principal with least privilege.
- GCP: Workload Identity Federation mapped to deployment service accounts.

Do not use long-lived cloud keys for the default workflow. Environment protection rules should require review before production plans and applies.
