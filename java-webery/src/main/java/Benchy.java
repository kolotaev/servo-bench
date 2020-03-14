package com.kolotaev;

import com.wizzardo.http.HttpConnection;
import com.wizzardo.http.framework.WebApplication;
import com.wizzardo.http.request.ByteTree;
import com.wizzardo.http.request.Header;
import com.wizzardo.http.request.Request;
import com.wizzardo.http.response.JsonResponseHelper;

public class Benchy {
    public static void main(String[] args) {
        WebApplication application = new WebApplication(args);

        application.onSetup(app -> {
                    app.getUrlMapping()
                            .append("/json", AppController.class, "json")
                            .append("/db", AppController.class, "db");
                }
        );

        application.start();
    }
}
