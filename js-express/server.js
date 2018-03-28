'use strict';

const express = require('express');
const { Pool } = require('pg')

const PORT = 8080;
const HOST = '0.0.0.0';


const sqlMaxSleep = parseInt(process.env.SQL_SLEEP_MAX) || 2 // seconds
const loopCount = parseInt(process.env.LOOP_COUNT) || 100


function randomString(len) {
    return Math.random().toString(36).substring(len);
}

function randomInt(max) {
    return Math.floor(Math.random() * max) + 1; 
}

function randomFloat() {
    return Math.random();
}


function createUser() {
    var friend = {
        name: randomString(10),
        surname: randomString(3),
        street: randomString(15),
        school: randomString(9),
        bank: randomString(4),
        a: randomInt(100),
        b: randomFloat(),
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
        b: randomFloat(),
        c: randomInt(1090),
        friend: friend,
    };
}

// App
const app = express();

// DB
const dbPool = new Pool({
  user: 'postgres',
  host: 'database_host',
  database: 'postgres',
  password: 'root',
  port: 5432,
})

// Routes
app.get('/json', (req, res) => {
    var user = createUser();
    res.json(user);
});

app.get('/db', (req, res) => {
    pool.query('SELECT pg_sleep($1)', [1], (err, res) => {
        if (err) {
            throw err;
        }
        pool.end();
    });

    // Create some CPU and RAM load
    var users = [];
    for (var i = 0; i < loopCount; i++) {
        users[i] = createUser();
    }

    var result = {
        "db-query": "",
        "data": users,
    }

    res.json(result);
});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);
