'use strict';

const express = require('express');
const { Pool } = require('pg');

const PORT = 8080;
const HOST = '0.0.0.0';


const sqlMaxSleep = parseInt(process.env.SQL_SLEEP_MAX) || 0; // seconds
const loopCount = parseInt(process.env.LOOP_COUNT) || 0;


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

// App
const app = express();

// DB
const pool = new Pool({
  user: 'postgres',
  host: '127.0.0.1',
  database: 'postgres',
  password: 'root',
  port: 5432,
  max: 250, // number of connection
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

app.get('/db', (req, res) => {
    // Make a DB call
    var randSleep = Math.random() * sqlMaxSleep;
    var qry = `SELECT pg_sleep(${randSleep})`;
    pool.query(qry, (err, result) => {
        if (err) {
            console.warn(err);
        }

        // Create some CPU and RAM load
        var users = [];
        for (var i = 0; i < loopCount; i++) {
            users[i] = createUser();
        }

        var resultData = {
            "db-query": qry,
            "data": users,
        };

        res.json(resultData);
    });
});

app.listen(PORT, HOST);
console.log(`Using SQL_SLEEP_MAX = ${sqlMaxSleep} seconds; LOOP_COUNT = ${loopCount}`);
console.log(`Running on http://${HOST}:${PORT}`);
