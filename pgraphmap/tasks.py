from __future__ import absolute_import, unicode_literals
from .cel import app
import redis
import os
import subprocess
import uuid
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


r = redis.Redis(
    host=os.environ['REDIS_HOST'],
    port=os.environ['REDIS_PORT'],
    password=os.environ['REDIS_PASS'])

storage_dir = os.environ.get("PGRAPHMAP_CACHE", '/var/tmp/graphmap/')
os.makedirs(storage_dir, exist_ok=True)


@app.task
def basecall(fastx, ref, circular, start, num):

    fpath = os.path.join(storage_dir, fastx)
    rpath = os.path.join(storage_dir, ref)

    if not os.path.exists(fpath):
        with open(fpath, 'wb') as f:
            f.write(r.get(fastx))

    if not os.path.exists(rpath):
        with open(rpath, 'wb') as f:
            f.write(r.get(ref))

    sam_id = str(uuid.uuid4()) + ".sam"
    spath = os.path.join(storage_dir, sam_id)

    args = ["graphmap", "align", "--start", str(start), "--numreads", str(num), "-r", rpath, "-d", fpath, "-o", spath, "-v", "0", "--extcigar"]
    if circular:
        args.append("--circular")
    print(args)
    subprocess.check_call(args)

    with open(spath, 'rb') as f:
        r.set(sam_id, f.read())

    return sam_id
