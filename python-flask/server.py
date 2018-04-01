import os
import random
import string

import psycopg2
from flask import Flask, render_template, jsonify



HOST = '0.0.0.0'
PORT = 8080
SLEEP_MAX = int(os.environ.get('SQL_SLEEP_MAX', 0))
LOOP_COUNT = int(os.environ.get('LOOP_COUNT', 0))


def random_string(max_len):
    return ''.join(random.choice(string.ascii_letters) for _ in range(max_len))


def create_user():
    return User(friend=User())


class User:
    def __init__(self, **kwargs):
        self.name: kwargs.get('name', random_string(10))
        self.surname: kwargs.get('surname', random_string(3))
        self.street: kwargs.get('street', random_string(15))
        self.school: kwargs.get('school', random_string(9))
        self.bank: kwargs.get('bank', random_string(4))
        self.a: kwargs.get('a', random.randint(0, 100))
        self.b: kwargs.get('b', random.random())
        self.c: kwargs.get('c', random.randint(0, 1090))
        self.friend: kwargs.get('friend', None)

    def __str__(self):
        return self.__dict__


try:
    db = 'dbname=postgres user=postgres password=rot host=127.0.0.1 '
    schema = "schema.sql"
    conn = psycopg2.connect(db)
    cur = conn.cursor()
except Exception as e:
    print(e)
    exit(1)


app = Flask(__name__)


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
    try:
        my_list = []
        if cur != None:
            cur.execute("""SELECT name from salesforce.contact""")
            rows = cur.fetchall()
            response = ''

            for row in rows:
                my_list.append(row[0])

        return render_template('template.html',  results=my_list)
    except Exception as e:
        print e
        return []


if __name__ == '__main__':
    app.run()
