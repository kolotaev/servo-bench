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
import io.vertx.pgclient.*;
import io.vertx.sqlclient.Pool;
import io.vertx.sqlclient.PoolOptions;
import io.vertx.sqlclient.Row;
import io.vertx.sqlclient.SqlConnection;


public class App extends AbstractVerticle implements Handler<HttpServerRequest> {

  private float sqlMaxSleep = Float.parseFloat(System.getenv("SQL_SLEEP_MAX"));
  private int loopCount = Integer.parseInt(System.getenv("LOOP_COUNT"));
  private int poolSize = Integer.parseInt(System.getenv("POOL_SIZE"));
  private Pool pool;

  public static void main(String[] args) {
    Vertx vertx = Vertx.vertx(
      new VertxOptions().setPreferNativeTransport(true)
    );
    vertx.exceptionHandler(err -> {
      err.printStackTrace();
    });
    vertx.deployVerticle(App.class.getName());
  }

  public void start() throws Exception {
    PgConnectOptions options = new PgConnectOptions();
    options.setDatabase("postgres")
        .setHost("127.0.0.1")
        .setPort(5432)
        .setUser("postgres")
        .setPassword("root");
    pool = PgPool.pool(vertx, options, new PoolOptions().setMaxSize(poolSize));

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

    pool.getConnection(ar1 -> {
      if (!ar1.succeeded()) {
        System.out.println("conn Failure: " + ar1.cause().getMessage());
        resp.end(Json.encode(ar1.cause().getMessage()));
        return;
      }
      SqlConnection conn = ar1.result();
      conn.query(q)
      .execute(dbRes -> {
        if (!dbRes.succeeded()) {
            System.out.println("Failure: " + dbRes.cause().getMessage());
            resp.end(Json.encode(dbRes.cause().getMessage()));
            conn.close();
            return;
        }
        for (int i = 0; i < this.loopCount; i++) {
            users.add(User.create(true));
        }
        result.put("users", users);
        result.put("query", q);
        // todo - use real result. Currently fails for transaction
        result.put("dbres", "dbRes.result().iterator().next()");

        resp.headers().add("content-type", "application/json");
        resp.end(Json.encode(result));
        conn.close();
      });
    });
  }

  private String getSqlQuery() {
      if (this.sqlMaxSleep >= 1000.0) {
          // simulate pgbench standard transactions run
          // before benchmarking, populate the DB with: pgbench -i -s100
          Random rnd = new Random();
          int scale = 100;
          int aid = rnd.nextInt(100000 * scale - 1) + 1;
          int bid = rnd.nextInt(1 * scale - 1) + 1;
          int tid = rnd.nextInt(10 * scale - 1) + 1;
          int delta = rnd.nextInt(10000)-5000;
          return "BEGIN;" +
          String.format("UPDATE pgbench_accounts SET abalance = abalance + %d WHERE aid = %d;", delta, aid) +
          String.format("SELECT abalance FROM pgbench_accounts WHERE aid = %d;", aid) +
          String.format("UPDATE pgbench_tellers SET tbalance = tbalance + %d WHERE tid = %d;", delta, tid) +
          String.format("UPDATE pgbench_branches SET bbalance = bbalance + %d WHERE bid = %d;", delta, bid) +
          String.format("INSERT INTO pgbench_history (tid, bid, aid, delta, mtime) VALUES (%d, %d, %d, %d, CURRENT_TIMESTAMP);", tid, bid, aid, delta) +
          "END;"; //  + "SELECT floor(random() * 1000);";
      } else if (this.sqlMaxSleep == 0.0) {
        // Very fast single query
        return "SELECT count(*) FROM pg_catalog.pg_user";
      }
      // A random sleep query
      return String.format("SELECT pg_sleep(%f)", new Random().nextDouble() * this.sqlMaxSleep);
  }
}
