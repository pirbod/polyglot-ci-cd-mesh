provider "aws"   { region = var.aws_region }
provider "azurerm"{ features {} }
provider "google"{ project = var.gcp_project; region = var.gcp_region }

module "aks"  { source = "./modules/cluster-aks";  prefix = var.prefix; location = var.azure_location }
module "eks"  { source = "./modules/cluster-eks";  prefix = var.prefix; region   = var.aws_region   }
module "gke"  { source = "./modules/cluster-gke";  prefix = var.prefix; region   = var.gcp_region   }
