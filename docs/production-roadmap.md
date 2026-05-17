# Production Roadmap

## Phase 1: Cloud Identity

- Configure GitHub OIDC for AWS, Azure, and GCP.
- Create separate roles for dev and prod.
- Add environment protection rules and approval gates.

## Phase 2: Terraform Resources

- Replace local module internals with AKS, EKS, and GKE resources.
- Add cloud registries and observability workspaces.
- Add remote state with encryption and locking.

## Phase 3: GitOps Operations

- Register real clusters in ArgoCD.
- Enable ApplicationSet generation for each cloud target.
- Add promotion branches or environment overlays.

## Phase 4: Supply Chain

- Enable keyless image signing.
- Store SBOM and provenance alongside release artifacts.
- Add admission policy checks for signatures and critical CVEs.

## Phase 5: Runtime Hardening

- Add network policies, pod security standards, resource quotas, and runtime alerts.
- Add gateway integration tests against Tyk policies.
