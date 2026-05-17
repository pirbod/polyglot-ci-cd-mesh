import test from 'node:test';
import assert from 'node:assert/strict';
import { servicePayload } from '../src/server.js';

test('service payload exposes expected metadata', () => {
  const payload = servicePayload();
  assert.equal(payload.service, 'node-service');
  assert.equal(payload.runtime, 'node');
  assert.equal(payload.version, '1.0.0');
});
