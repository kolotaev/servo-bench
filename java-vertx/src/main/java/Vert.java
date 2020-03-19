package com.kolotaev;

import io.vertx.core.*;
import io.vertx.core.http.HttpServer;
import io.vertx.core.http.HttpServerOptions;
import io.vertx.core.http.HttpServerRequest;
import io.vertx.core.http.HttpServerResponse;
import io.vertx.core.http.HttpHeaders;
import io.vertx.core.json.Json;
import io.vertx.core.json.JsonArray;


public class Vert extends AbstractVerticle implements Handler<HttpServerRequest> {

  public static void main(String[] args) {
    Vertx vertx = Vertx.vertx(new VertxOptions().setPreferNativeTransport(true));
    vertx.exceptionHandler(err -> {
      err.printStackTrace();
    });
    vertx.deployVerticle(Vert.class.getName());
  }

  public void start() throws Exception {
    vertx.createHttpServer(new HttpServerOptions())
      .requestHandler(Vert.this).listen(8080);
  }

  @Override
  public void handle(HttpServerRequest request) {
    switch (request.path()) {
      case "/json":
        handleJson(request);
        break;
      case "/db":
        handleDb(request);
        break;
      default:
        request.response().setStatusCode(404);
        request.response().end();
        break;
    }
  }

  private void handleJson(HttpServerRequest request) {
    HttpServerResponse response = request.response();
    response.headers().add("content-type", "application/json");
    User user = User.create(true);
    response.end(Json.encode(user));
  }

  private void handleDb(HttpServerRequest request) {
    HttpServerResponse response = request.response();
    response.headers().add("content-type", "application/json");
    User user = User.create(true);
    response.end(Json.encode(user));
  }
}
