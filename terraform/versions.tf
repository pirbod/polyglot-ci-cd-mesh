terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.70"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.6"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 6.5"
    }
  }
}

provider "aws" {
  region                      = var.aws_region
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true
}

provider "azurerm" {
  features {}
  skip_provider_registration = true
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}
