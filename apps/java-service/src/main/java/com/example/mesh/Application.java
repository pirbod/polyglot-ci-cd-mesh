package com.example.mesh;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Map;
import java.util.stream.Collectors;

public class Application {
  private static final String SERVICE = "java-service";
  private static final String VERSION = "1.0.0";
  private static final String RUNTIME = "java";

  public static void main(String[] args) throws IOException {
    int port = Integer.parseInt(System.getenv().getOrDefault("PORT", "8081"));
    HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);
    server.createContext("/health", exchange -> writeJson(exchange, healthPayload()));
    server.createContext("/version", exchange -> writeJson(exchange, versionPayload()));
    server.start();
  }

  static String healthPayload() {
    return payload(Map.of("status", "ok"));
  }

  static String versionPayload() {
    return payload(Map.of("status", "ok"));
  }

  static String payload(Map<String, String> fields) {
    Map<String, String> values = new java.util.LinkedHashMap<>();
    values.put("service", SERVICE);
    values.put("version", VERSION);
    values.put("runtime", RUNTIME);
    values.put("environment", System.getenv().getOrDefault("ENVIRONMENT", "local"));
    values.put("build", System.getenv().getOrDefault("BUILD_SHA", "local"));
    values.put("timestamp", Instant.now().toString());
    values.putAll(fields);
    return values.entrySet().stream()
        .map(entry -> "\"" + entry.getKey() + "\":\"" + entry.getValue() + "\"")
        .collect(Collectors.joining(",", "{", "}"));
  }

  private static void writeJson(HttpExchange exchange, String body) throws IOException {
    byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
    exchange.getResponseHeaders().add("Content-Type", "application/json");
    exchange.sendResponseHeaders(200, bytes.length);
    exchange.getResponseBody().write(bytes);
    exchange.close();
  }
}
