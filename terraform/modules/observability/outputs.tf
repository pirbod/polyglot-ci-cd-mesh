output "workspace_name" {
  description = "Observability workspace name."
  value       = local.workspace_name
}

output "cluster_count" {
  description = "Number of clusters connected to observability."
  value       = length(var.clusters)
}
