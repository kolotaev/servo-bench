import asyncio
import json as JSON
import os
import random
import string

from aiohttp import web
import peewee
import peewee_async


HOST = '0.0.0.0'
PORT = 8080
SLEEP_MAX = int(os.environ.get('SQL_SLEEP_MAX', 0))
LOOP_COUNT = int(os.environ.get('LOOP_COUNT', 0))

dsn = 'dbname=postgres user=postgres password=root host=127.0.0.1'
database = peewee_async.PooledPostgresqlDatabase('postgres', max_connections=250, dsn=dsn)


class Model(peewee.Model):
    content = peewee.CharField(max_length=512)

    class Meta:
        database = database


def random_string(max_len):
    return ''.join(random.choice(string.ascii_letters) for _ in range(max_len))


def create_user():
    return User(friend=User())


def jsonify(data):
    return JSON.dumps(data, cls=MyJSONEncoder)


class MyJSONEncoder(JSON.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.__dict__
        return super().default(obj)


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


@asyncio.coroutine
def json(_):
    user = create_user()
    return web.Response(text=jsonify(user), content_type='application/json')


@asyncio.coroutine
def db(_):
    qry = 'SELECT pg_sleep(%f)' % random.uniform(0, SLEEP_MAX)
    items = yield from peewee_async.execute(Model.raw(qry))
    list(items)
    users = []
    for i in range(LOOP_COUNT):
        user = create_user()
        users.append(user)
    return web.Response(
        text=jsonify(jsonify({'db-query': qry, 'data': users})),
        content_type='application/json')


app = web.Application()
app.router.add_route('GET', '/json', json)
app.router.add_route('GET', '/db', db)

loop = asyncio.get_event_loop()
loop.run_until_complete(database.connect_async(loop=loop))
