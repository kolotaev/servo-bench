package com.kolotaev;

import java.util.List;
import java.util.Map;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;
import java.nio.charset.Charset;
import com.wizzardo.epoll.ByteBufferProvider;
import com.wizzardo.epoll.ByteBufferWrapper;
import com.wizzardo.http.HttpConnection;
import com.wizzardo.http.framework.Controller;
import com.wizzardo.http.request.Request;
import com.wizzardo.http.response.Status;
import com.wizzardo.http.response.JsonResponseHelper;
import com.wizzardo.http.request.Header;
import com.wizzardo.tools.json.JsonTools;


public class AppController extends Controller {

    private float sqlMaxSleep = Float.parseFloat(System.getenv("SQL_SLEEP_MAX"));
    private int loopCount = Integer.parseInt(System.getenv("LOOP_COUNT"));
    private DB db = new DB();

    static class User {
        public String name;
        public String surname;
        public String street;
        public String school;
        public String bank;
        public int a;
        public double b;
        public int c;
        public List<User> friends;

        public User(String name, String surname, String street,
                    String school, String bank, int a, double b, int c) {
            this.name = name;
            this.surname = surname;
            this.street = street;
            this.school = school;
            this.bank = bank;
            this.a = a;
            this.b = b;
            this.c = c;
            this.friends = new ArrayList<User>();
        }

        public static User create(boolean withFriend) {
            User u = new User(
                randomString(10),
                randomString(3),
                randomString(15),
                randomString(9),
                randomString(4),
                new Random().nextInt(100),
                new Random().nextDouble(),
                new Random().nextInt(100)
            );
            if (withFriend) u.friends.add(create(false));
            return u;
        }

        private static String randomString(int len) {
            return new Random().ints(97, 123)
              .limit(len)
              .collect(StringBuilder::new, StringBuilder::appendCodePoint, StringBuilder::append)
              .toString();
        }
    }

    void json() {
        User user = User.create(true);
        response.setBody(JsonResponseHelper.renderJson(user))
                .appendHeader(Header.KV_CONTENT_TYPE_APPLICATION_JSON);
    }

    void db() {
        response.async();
        Map<String, Object> res = new HashMap<>();
        List<User> users = new ArrayList<User>();
        String q = getSqlQuery();

        db.getClient().query(q, dbRes -> {
            for (int i = 0; i < this.loopCount; i++) {
                users.add(User.create(true));
            }
            res.put("users", users);
            res.put("query", q);
            res.put("dbres", dbRes);
            response.appendHeader(Header.KV_CONTENT_TYPE_APPLICATION_JSON);
            response.body(JsonTools.serializeToBytes(res));
            commitAsyncResponse();
        });
    }

    private String getSqlQuery() {
        if (this.sqlMaxSleep == 0.0) {
            return "SELECT count(*) FROM pg_catalog.pg_user";
        }
        return String.format("SELECT pg_sleep(%f)", new Random().nextDouble() * this.sqlMaxSleep);
    }

    static ThreadLocal<ByteBufferProvider> byteBufferProviderThreadLocal = ThreadLocal.<ByteBufferProvider>withInitial(() -> {
        ByteBufferWrapper wrapper = new ByteBufferWrapper(64 * 1024);
        return () -> wrapper;
    });

    protected void commitAsyncResponse() {
        ByteBufferProvider bufferProvider = byteBufferProviderThreadLocal.get();
        HttpConnection connection = request.connection();
        response.commit(connection, bufferProvider);
        connection.flush(bufferProvider);
        response.reset();
    }
}
