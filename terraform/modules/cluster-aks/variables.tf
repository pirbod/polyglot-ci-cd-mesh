variable "prefix" {
  description = "Resource prefix."
  type        = string
}

variable "environment" {
  description = "Environment name."
  type        = string
}

variable "location" {
  description = "Azure location."
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
