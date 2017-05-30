from __future__ import absolute_import, unicode_literals
from celery import Celery
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

rbkd = r"redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}".format(**os.environ)

app = Celery('proj',
             broker=rbkd,
             backend=rbkd,
             include=['pgraphmap.tasks'])

if __name__ == '__main__':
    app.start()
