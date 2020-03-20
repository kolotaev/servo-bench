package com.kolotaev;

import java.util.List;
import java.util.Map;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

import io.vertx.core.*;
import io.vertx.core.http.HttpServer;
import io.vertx.core.http.HttpServerOptions;
import io.vertx.core.http.HttpServerRequest;
import io.vertx.core.http.HttpServerResponse;
import io.vertx.core.http.HttpHeaders;
import io.vertx.core.json.Json;
import io.vertx.core.json.JsonArray;
import io.reactiverse.pgclient.*;


public class App extends AbstractVerticle implements Handler<HttpServerRequest> {

  private float sqlMaxSleep = Float.parseFloat(System.getenv("SQL_SLEEP_MAX"));
  private int loopCount = Integer.parseInt(System.getenv("LOOP_COUNT"));
  private int poolSize = Integer.parseInt(System.getenv("POOL_SIZE"));
  private PgPool pool;
  private PgClient client;

  public static void main(String[] args) {
    Vertx vertx = Vertx.vertx(
      new VertxOptions()
      .setPreferNativeTransport(true)
      // .setBlockedThreadCheckInterval(5000L)
      // .setMaxWorkerExecuteTime(50000000000L)
      // .setMaxEventLoopExecuteTime(50000000000L)
      // .setWorkerPoolSize(400)
    );
    vertx.exceptionHandler(err -> {
      err.printStackTrace();
    });
    vertx.deployVerticle(App.class.getName());
  }

  public void start() throws Exception {
    PgPoolOptions options = new PgPoolOptions();
    options.setDatabase("postgres")
        .setHost("127.0.0.1")
        .setPort(5432)
        .setUser("postgres")
        .setPassword("root")
        .setMaxSize(poolSize);
    // pool = PgClient.pool(vertx, options);
    // client = PgClient.pool(vertx, new PgPoolOptions(options).setMaxSize(1));
    client = PgClient.pool(vertx, options);

    vertx.createHttpServer(new HttpServerOptions())
      .requestHandler(App.this).listen(8080);
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
    HttpServerResponse resp = request.response();
    User user = User.create(true);
    resp.headers().add("content-type", "application/json");
    resp.end(Json.encode(user));
  }

  private void handleDb(HttpServerRequest request) {
    HttpServerResponse resp = request.response();
    Map<String, Object> result = new HashMap<>();
    List<User> users = new ArrayList<User>();
    String q = getSqlQuery();

    client.query(q, dbRes -> {
      for (int i = 0; i < this.loopCount; i++) {
          users.add(User.create(true));
      }
      result.put("users", users);
      result.put("query", q);
      result.put("dbres", dbRes.result().iterator().next());

      resp.headers().add("content-type", "application/json");
      resp.end(Json.encode(result));
    });
  }

  private String getSqlQuery() {
      if (this.sqlMaxSleep == 0.0) {
          return "SELECT count(*) FROM pg_catalog.pg_user";
      }
      return String.format("SELECT pg_sleep(%f)", new Random().nextDouble() * this.sqlMaxSleep);
  }
}
