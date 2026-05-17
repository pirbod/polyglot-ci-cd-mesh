package mesh.api

deny[msg] {
  not input.components.securitySchemes
  msg := "API must define at least one auth scheme"
}

deny[msg] {
  some path
  contains(lower(path), "admin")
  operation := input.paths[path][_]
  operation["x-public"] == true
  msg := sprintf("admin path must not be public: %s", [path])
}

deny[msg] {
  not input["x-tyk-rate-limit"]
  not input["x-rate-limit"]
  msg := "API must define a gateway rate limit"
}

deny[msg] {
  not input["x-service-metadata"].owner
  msg := "service owner metadata is required"
}

deny[msg] {
  not input["x-service-metadata"].runtime
  msg := "service runtime metadata is required"
}

deny[msg] {
  not input["x-service-metadata"].criticality
  msg := "service criticality metadata is required"
}
