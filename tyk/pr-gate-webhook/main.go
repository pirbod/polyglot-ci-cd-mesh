package main

import (
  "encoding/json"
  "net/http"
  "os"
)

type PRPayload struct {
  Repo string `json:"repo"`
  PR   int    `json:"pr"`
}

func main() {
  http.HandleFunc("/validate", func(w http.ResponseWriter, r *http.Request) {
    var p PRPayload
    _ = json.NewDecoder(r.Body).Decode(&p)
    // TODO: call Tyk Management API to fetch policies & validate OpenAPI spec
    // respond 200 OK if compliant, 422 otherwise
    w.WriteHeader(http.StatusOK)
    w.Write([]byte(`{"status":"compliant"}`))
  })
  http.ListenAndServe(":"+os.Getenv("PORT"), nil)
}
