output "cluster_name" {
  description = "GKE cluster name."
  value       = local.cluster_name
}

output "target" {
  description = "GKE target metadata."
  value = {
    cloud              = "gcp"
    region             = var.region
    kubernetes_version = var.kubernetes_version
    allowed_cidrs      = var.allowed_cidrs
  }
}
