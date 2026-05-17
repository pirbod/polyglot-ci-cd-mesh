# Local Demo

The local demo is the default path and requires no paid cloud resources.

## Commands

```bash
make install
make test
make demo-check
make screenshots
make validate
make demo
```

## Ports

| Component | URL |
| --- | --- |
| Dashboard UI | http://localhost:5173 |
| Dashboard API | http://localhost:8080 |
| API policy gate | http://localhost:8090 |
| Java service | http://localhost:8081/health |
| .NET service | http://localhost:8082/health |
| Node.js service | http://localhost:8083/health |
| Python service | http://localhost:8084/health |

## Evidence

Generated reports live in `evidence/` and are exposed by the dashboard Evidence Center.
