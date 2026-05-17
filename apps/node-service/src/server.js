import express from 'express';

export function servicePayload(status = 'ok') {
  return {
    service: 'node-service',
    version: '1.0.0',
    runtime: 'node',
    environment: process.env.ENVIRONMENT || 'local',
    build: process.env.BUILD_SHA || 'local',
    timestamp: new Date().toISOString(),
    status,
  };
}

export function createApp() {
  const app = express();
  app.get('/health', (_request, response) => response.json(servicePayload('ok')));
  app.get('/version', (_request, response) => response.json(servicePayload('ok')));
  return app;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const port = Number(process.env.PORT || 8083);
  createApp().listen(port, () => {
    console.log(`node-service listening on ${port}`);
  });
}
