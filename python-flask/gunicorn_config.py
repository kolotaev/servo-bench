from multiprocessing import cpu_count
from psycogreen.gevent import patch_psycopg


bind = '0.0.0.0:8080'
max_requests = 10000
worker_class = 'gevent'
workers = cpu_count() + 1


def post_fork(server, worker):
    patch_psycopg()
    worker.log.info("Made Psycopg2 Green")
