variable "prefix" {
  description = "Resource prefix."
  type        = string
}

variable "environment" {
  description = "Environment name."
  type        = string
}

variable "clusters" {
  description = "Cluster names included in the workspace."
  type        = map(string)
}
