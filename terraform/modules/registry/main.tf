locals {
  registries = {
    for cloud in var.clouds : cloud => "${var.prefix}-${cloud}-${var.environment}.registry.local"
  }
}
