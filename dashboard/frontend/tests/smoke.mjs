import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const app = readFileSync(new URL('../src/App.tsx', import.meta.url), 'utf8');
const requiredLabels = [
  'Executive',
  'Pipelines',
  'Cloud',
  'API Gate',
  'Supply Chain',
  'GitOps',
  'Evidence',
];

for (const label of requiredLabels) {
  assert.ok(app.includes(label), `missing dashboard label: ${label}`);
}

assert.ok(app.includes('/api/pipelines/run'), 'pipeline action endpoint is missing');
assert.ok(app.includes('/api/openapi/select'), 'OpenAPI gate endpoint is missing');
assert.ok(app.includes('/api/gitops/rollback'), 'rollback endpoint is missing');
console.log('frontend smoke test passed');
