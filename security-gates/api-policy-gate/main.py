from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from policy_gate import validate_openapi


class OpenApiPayload(BaseModel):
    spec: dict | str


app = FastAPI(title="API Policy Gate", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "api-policy-gate"}


@app.post("/validate-openapi")
async def validate_openapi_endpoint(payload: OpenApiPayload | None = None, file: UploadFile | None = File(default=None)):
    if file is not None:
        raw = await file.read()
        return validate_openapi(raw)
    if payload is None:
        raise HTTPException(status_code=400, detail="Provide a JSON payload or uploaded OpenAPI file.")
    return validate_openapi(payload.spec)
