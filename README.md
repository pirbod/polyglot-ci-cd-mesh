# Polyglot CI/CD Mesh

**Unify build, test & delivery** for Java, .NET, Node.js and Python across AKS, EKS & GKE—powered by GitHub Actions, Terraform modules and ArgoCD.

## Core Capabilities
- **Matrix CI/CD**: Parallel workflows for Maven, dotnet, npm and pytest via GitHub Actions.
- **Multi-Arch Docker**: Buildx pipelines produce ARM & AMD images from a single codebase.
- **Cross-Cloud Infra**: Terraform modules spin up AKS/EKS/GKE on demand.
- **GitOps Delivery**: ArgoCD apps-of-apps pattern instantiates per-team pipelines.
- **API Security Gate**: Tyk webhook enforces policy-as-code in PRs before merge.

## Tech Stack & Flow
1. **GitHub Actions**  
   - Matrix job builds & tests each runtime  
   - Docker Buildx pushes multi-arch images to each cloud registry  
   - Tyk PR-gate webhook validates OpenAPI & policy rules
2. **Terraform Modules**  
   - `cluster-aks`, `cluster-eks`, `cluster-gke` provision clusters with best-practice defaults  
3. **ArgoCD Apps-of-Apps**  
   - Root app deploys per-team `sample-app` charts into respective clusters  
4. **Tyk Integration**  
   - Go-based webhook enforces gateway policies on every API change

## Prerequisites
- GitHub repo with Secrets:  
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AZURE
    - GCP
- Docker Buildx enabled  
- ArgoCD controller installed in each target cluster  
- Tyk Gateway endpoint & credentials  

##  Quickstart
1. `git clone` & fill in `terraform/variables.tf`.  
2. `cd terraform && terraform init && terraform apply` (provisions all three clusters).  
3. Create a branch & modify `charts/sample-app/values.yaml` with your image.  
4. Open a PR → GitHub Actions runs matrix → multi-arch images land in registries.  
5. On PR, Tyk webhook validates API spec.  
6. Merge → ArgoCD apps-of-apps picks it up & deploys to all clusters.
