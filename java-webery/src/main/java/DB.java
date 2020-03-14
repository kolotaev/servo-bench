package com.kolotaev;

import io.reactiverse.pgclient.PgPool;
import io.reactiverse.pgclient.impl.WizzardoPgPool;
import io.reactiverse.pgclient.impl.WizzardoPgPoolOptions;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.SQLException;

public class DB {

    protected DataSource dataSource;

    protected ThreadLocal<PgPool> clientThreadLocal = ThreadLocal.withInitial(this::initPgPool);

    protected PgPool initPgPool() {
        int poolSize = Integer.parseInt(System.getenv("POOL_SIZE"));
        WizzardoPgPoolOptions options = new WizzardoPgPoolOptions();
        options.setDatabase("postgres");
        options.setHost("127.0.0.1");
        options.setPort(5432);
        options.setUser("postgres");
        options.setPassword("root");
        options.setCachePreparedStatements(true);
        // explicitly set 1 to fence against OutOfMemoryError
        options.setMaxSize(1);
        return new WizzardoPgPool(options);
    }

    public Connection getConnection() throws SQLException {
        return dataSource.getConnection();
    }

    public PgPool getClient() {
        return clientThreadLocal.get();
    }
}
