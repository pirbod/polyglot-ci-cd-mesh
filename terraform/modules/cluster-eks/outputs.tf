output "cluster_name" {
  description = "EKS cluster name."
  value       = local.cluster_name
}

output "target" {
  description = "EKS target metadata."
  value = {
    cloud              = "aws"
    region             = var.region
    kubernetes_version = var.kubernetes_version
    allowed_cidrs      = var.allowed_cidrs
  }
}
