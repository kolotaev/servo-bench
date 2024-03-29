'use strict';

const express = require('express');
const { Pool } = require('pg');
const axios = require('axios');

const PORT = 8080;
const HOST = '0.0.0.0';

const sqlMaxSleep = parseFloat(process.env.SQL_SLEEP_MAX) || 0.0; // seconds
const loopCount = parseInt(process.env.LOOP_COUNT) || 0;
const poolSize = parseInt(process.env.POOL_SIZE) || 1;
const targetUrl = process.env.TARGET_URL.replace(/\/$/, '');


function randomString(len) {
    return Math.random().toString(36).substring(len);
}

function randomInt(max) {
    return Math.floor(Math.random() * max) + 1;
}


function createUser() {
    var friend = {
        name: randomString(10),
        surname: randomString(3),
        street: randomString(15),
        school: randomString(9),
        bank: randomString(4),
        a: randomInt(100),
        b: Math.random(),
        c: randomInt(1090),
        friend: null,
    };
    return {
        name: randomString(10),
        surname: randomString(3),
        street: randomString(15),
        school: randomString(9),
        bank: randomString(4),
        a: randomInt(100),
        b: Math.random(),
        c: randomInt(1090),
        friend: friend,
    };
}

function randSleep() {
    return Math.random() * sqlMaxSleep;
}

// App
const app = express();

// DB
const pool = new Pool({
  user: 'postgres',
  host: '127.0.0.1',
  database: 'postgres',
  password: 'root',
  port: 5432,
  max: poolSize, // number of connections
});

// Routes
app.get('/', (req, res) => {
    res.write("<html>It's me, Express App.<br/>");
    res.write("Use routes:<br/><a href='./json'>json</a><br/>");
    res.write("<a href='./db'>db</a></html>");
    res.end();
});

app.get('/json', (req, res) => {
    var user = createUser();
    res.json(user);
});

app.get('/http', (req, res) => {
    axios.get(`${targetUrl}/${randSleep()}`)
    .then(result => res.json(result.data))
    .catch(err => res.status(500).json(err));
});

app.get('/db', (req, res) => {
    // Make a DB call
    var qry = "";
    if (sqlMaxSleep == 0) {
      qry = "SELECT count(*) FROM pg_catalog.pg_user"
    } else {
      qry = `SELECT pg_sleep(${randSleep()})`;
    }
    pool.query(qry, (err, result) => {
        if (err) {
            console.warn(err);
            res.status(500).json(err);
        }

        // Create some CPU and RAM load
        var users = [];
        for (var i = 0; i < loopCount; i++) {
            users[i] = createUser();
        }

        var resultData = {
            "db-query": qry,
            "data": users,
            "result": result,
        };

        res.json(resultData);
    });
});

app.listen(PORT, HOST);
console.log(`Using SQL_SLEEP_MAX = ${sqlMaxSleep} seconds; LOOP_COUNT = ${loopCount}`);
console.log(`Running on http://${HOST}:${PORT}`);
