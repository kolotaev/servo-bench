'use strict';

const express = require('express');

const PORT = 8080;
const HOST = '0.0.0.0';


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

app.get('/json', (req, res) => {
    var user = createUser();
    res.json(user);
});

app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);
