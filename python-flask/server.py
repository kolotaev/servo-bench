import os
import sys
import random
import string
import logging
from contextlib import contextmanager

import psycopg2.pool
from flask import Flask, jsonify
from flask.json import JSONEncoder


HOST = '0.0.0.0'
PORT = 8080
SLEEP_MAX = int(os.environ.get('SQL_SLEEP_MAX', 0))
LOOP_COUNT = int(os.environ.get('LOOP_COUNT', 0))


def random_string(max_len):
    return ''.join(random.choice(string.ascii_letters) for _ in range(max_len))


def create_user():
    return User(friend=User())


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.__dict__
        return super().default(obj)


@contextmanager
def get_cursor():
    global pool
    con = pool.getconn()
    try:
        yield con.cursor()
    finally:
        pool.putconn(con)


class User:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', random_string(10))
        self.surname = kwargs.get('surname', random_string(3))
        self.street = kwargs.get('street', random_string(15))
        self.school = kwargs.get('school', random_string(9))
        self.bank = kwargs.get('bank', random_string(4))
        self.a = kwargs.get('a', random.randint(0, 100))
        self.b = kwargs.get('b', random.random())
        self.c = kwargs.get('c', random.randint(0, 1090))
        self.friend = kwargs.get('friend', None)


# ======= Main ======= #

app = Flask(__name__)
app.json_encoder = MyJSONEncoder
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
app.logger.error('Using SQL_SLEEP_MAX = %i seconds; LOOP_COUNT = %i' % (SLEEP_MAX, LOOP_COUNT))
try:
    dsn = 'dbname=postgres user=postgres password=root host=127.0.0.1 '
    pool = psycopg2.pool.SimpleConnectionPool(1, 250, dsn=dsn)
except Exception as e:
    app.logger.error(e)
    sys.exit(e)


# ====== Routes ====== #

@app.route('/')
def home():
    return """
    <html>It's me, Flask App.<br/>
    Use routes:<br/><a href='./json'>json</a><br/>
    <a href='./db'>db</a></html>
    """


@app.route('/json')
def json():
    user = create_user()
    return jsonify(user)


@app.route('/db')
def db():
    qry = 'SELECT pg_sleep(%f)' % random.uniform(0, SLEEP_MAX)
    with get_cursor() as cur:
        cur.execute(qry)
        cur.fetchall()
    users = []
    for i in range(LOOP_COUNT):
        user = create_user()
        users.append(user)
    return jsonify({'db-query': qry, 'data': users})


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
