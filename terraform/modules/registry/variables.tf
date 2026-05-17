variable "prefix" {
  description = "Resource prefix."
  type        = string
}

variable "environment" {
  description = "Environment name."
  type        = string
}

variable "clouds" {
  description = "Cloud target identifiers."
  type        = list(string)
}
