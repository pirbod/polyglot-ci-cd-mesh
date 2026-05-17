from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from data import ROOT, list_evidence, load_state, promote, rollback, run_pipeline


class PipelineRequest(BaseModel):
    service_id: str


class PromotionRequest(BaseModel):
    environment: str = "prod"


class RollbackRequest(BaseModel):
    app_id: str


class OpenApiSelection(BaseModel):
    filename: str


app = FastAPI(title="Polyglot CI/CD Mesh Dashboard API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "dashboard-api"}


@app.get("/api/state")
def state() -> dict[str, Any]:
    current = load_state()
    current["evidence"] = list_evidence()
    return current


@app.post("/api/pipelines/run")
def run_pipeline_endpoint(request: PipelineRequest) -> dict[str, Any]:
    try:
        return run_pipeline(request.service_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Unknown service") from exc


@app.post("/api/clouds/promote")
def promote_endpoint(request: PromotionRequest) -> dict[str, Any]:
    return promote(request.environment)


@app.post("/api/gitops/rollback")
def rollback_endpoint(request: RollbackRequest) -> dict[str, Any]:
    try:
        return rollback(request.app_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Unknown application") from exc


@app.post("/api/openapi/select")
def select_openapi(request: OpenApiSelection) -> dict[str, Any]:
    from sys import path

    gate_dir = ROOT / "security-gates" / "api-policy-gate"
    if str(gate_dir) not in path:
        path.insert(0, str(gate_dir))
    from policy_gate import validate_file

    spec_path = ROOT / "security-gates" / "openapi-rules" / request.filename
    if not spec_path.exists():
        raise HTTPException(status_code=404, detail="Unknown OpenAPI sample")
    return validate_file(spec_path)


@app.get("/api/evidence")
def evidence() -> list[dict[str, str]]:
    return list_evidence()


@app.get("/api/evidence/{name}")
def download_evidence(name: str):
    path = ROOT / "evidence" / name
    if not path.exists() or path.parent != ROOT / "evidence":
        raise HTTPException(status_code=404, detail="Evidence file not found")
    return FileResponse(Path(path), filename=name, media_type="application/json")
