variable "prefix" {
  description = "Resource prefix."
  type        = string
}

variable "environment" {
  description = "Environment name."
  type        = string
}

variable "region" {
  description = "GCP region."
  type        = string
}

variable "kubernetes_version" {
  description = "Kubernetes version."
  type        = string
}

variable "allowed_cidrs" {
  description = "Allowed control-plane CIDRs."
  type        = list(string)
}
