variable "prefix" {
  description = "Short lowercase resource prefix used by all local and cloud examples."
  type        = string
  default     = "polyglot"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{2,24}$", var.prefix))
    error_message = "Prefix must be lowercase, start with a letter, and contain only letters, numbers, and dashes."
  }
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "local"

  validation {
    condition     = contains(["local", "dev", "prod"], var.environment)
    error_message = "Environment must be local, dev, or prod."
  }
}

variable "aws_region" {
  description = "AWS region for the EKS production path."
  type        = string
  default     = "eu-central-1"
}

variable "azure_location" {
  description = "Azure region for the AKS production path."
  type        = string
  default     = "westeurope"
}

variable "gcp_project" {
  description = "GCP project id for the GKE production path. The local demo does not use this value."
  type        = string
  default     = "example-gcp-project"
}

variable "gcp_region" {
  description = "GCP region for the GKE production path."
  type        = string
  default     = "europe-west3"
}

variable "kubernetes_version" {
  description = "Target Kubernetes minor version for cluster examples."
  type        = string
  default     = "1.30"
}

variable "allowed_cidrs" {
  description = "CIDR ranges allowed to reach control-plane endpoints in real deployments."
  type        = list(string)
  default     = ["10.0.0.0/8"]

  validation {
    condition     = length(var.allowed_cidrs) > 0
    error_message = "At least one allowed CIDR must be supplied."
  }
}
