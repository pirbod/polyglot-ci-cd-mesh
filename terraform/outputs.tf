output "cluster_targets" {
  description = "Local validation view of the three target clusters."
  value = {
    aks = module.aks.cluster_name
    eks = module.eks.cluster_name
    gke = module.gke.cluster_name
  }
}

output "registry_targets" {
  description = "Registry endpoints used by the delivery model."
  value       = module.registry.registries
}

output "observability_workspace" {
  description = "Observability workspace name for the mesh."
  value       = module.observability.workspace_name
}
