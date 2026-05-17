output "cluster_name" {
  description = "AKS cluster name."
  value       = local.cluster_name
}

output "target" {
  description = "AKS target metadata."
  value = {
    cloud              = "azure"
    location           = var.location
    kubernetes_version = var.kubernetes_version
    allowed_cidrs      = var.allowed_cidrs
  }
}
