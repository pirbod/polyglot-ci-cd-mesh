module "aks" {
  source             = "./modules/cluster-aks"
  prefix             = var.prefix
  environment        = var.environment
  location           = var.azure_location
  kubernetes_version = var.kubernetes_version
  allowed_cidrs      = var.allowed_cidrs
}

module "eks" {
  source             = "./modules/cluster-eks"
  prefix             = var.prefix
  environment        = var.environment
  region             = var.aws_region
  kubernetes_version = var.kubernetes_version
  allowed_cidrs      = var.allowed_cidrs
}

module "gke" {
  source             = "./modules/cluster-gke"
  prefix             = var.prefix
  environment        = var.environment
  region             = var.gcp_region
  kubernetes_version = var.kubernetes_version
  allowed_cidrs      = var.allowed_cidrs
}

module "registry" {
  source      = "./modules/registry"
  prefix      = var.prefix
  environment = var.environment
  clouds      = ["aks", "eks", "gke"]
}

module "observability" {
  source      = "./modules/observability"
  prefix      = var.prefix
  environment = var.environment
  clusters = {
    aks = module.aks.cluster_name
    eks = module.eks.cluster_name
    gke = module.gke.cluster_name
  }
}
