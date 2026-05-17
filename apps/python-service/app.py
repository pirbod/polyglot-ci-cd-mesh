from __future__ import annotations

from datetime import datetime, timezone
import os

from fastapi import FastAPI


SERVICE = "python-service"
VERSION = "1.0.0"
RUNTIME = "python"

app = FastAPI(title="Python Service API", version=VERSION)


def service_payload(status: str = "ok") -> dict[str, str]:
    return {
        "service": SERVICE,
        "version": VERSION,
        "runtime": RUNTIME,
        "environment": os.getenv("ENVIRONMENT", "local"),
        "build": os.getenv("BUILD_SHA", "local"),
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": status,
    }


@app.get("/health")
def health() -> dict[str, str]:
    return service_payload("ok")


@app.get("/version")
def version() -> dict[str, str]:
    return service_payload("ok")
