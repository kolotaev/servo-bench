import asyncio
import json as JSON
import os
import random
import string

from aiohttp import web
import uvloop
import asyncpg


HOST = '0.0.0.0'
PORT = 8080
SLEEP_MAX = float(os.environ.get('SQL_SLEEP_MAX', 0.0))
LOOP_COUNT = int(os.environ.get('LOOP_COUNT', 0))
POOL_SIZE = int(os.environ.get('POOL_SIZE', 1))
DSN = 'postgres://postgres:root@127.0.0.1:5432/postgres'


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


async def setup_db(loop):
    return await asyncpg.create_pool(DSN, loop=loop, max_size=POOL_SIZE)


async def startup(app):
    app['db'] = await setup_db(app.loop)


async def cleanup(app):
    await app['db'].close()


async def json(_):
    user = create_user()
    return web.Response(text=jsonify(user), content_type='application/json')


async def db(request):
    if SLEEP_MAX == 0:
        qry = "SELECT count(*) FROM pg_catalog.pg_user"
    else:
        qry = 'SELECT pg_sleep(%f)' % random.uniform(0, SLEEP_MAX)
    async with request.app['db'].acquire() as conn:
        result = await conn.fetchval(qry)
    users = []
    for i in range(LOOP_COUNT):
        user = create_user()
        users.append(user)
    return web.Response(
        text=jsonify({'db-query': qry, 'data': users, 'result': result}),
        content_type='application/json')


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    web_app = web.Application()
    web_app.on_startup.append(startup)
    web_app.on_cleanup.append(cleanup)
    web_app.router.add_route('GET', '/json', json)
    web_app.router.add_route('GET', '/db', db)
    web.run_app(web_app, port=PORT, access_log=None)
