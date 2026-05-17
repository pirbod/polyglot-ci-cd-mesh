package com.example.mesh;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

class ApplicationTest {
  @Test
  void healthPayloadIncludesServiceMetadata() {
    String payload = Application.healthPayload();
    assertTrue(payload.contains("\"service\":\"java-service\""));
    assertTrue(payload.contains("\"runtime\":\"java\""));
    assertTrue(payload.contains("\"version\":\"1.0.0\""));
  }
}
