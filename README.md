# pgraphmap
Simple multimachine graphmap

# Installation

## Server

Start redis server somewhere, for example with docker:
```docker run -p 6379:6379 --rm redis redis-server --requirepass <password>```

On each worker machine following environment variables must be set:

```
REDIS_PASS
REDIS_HOST
REDIS_PORT
```

Optionally ```PGRAPHMAP_CACHE``` set for caching different than default ```/var/tmp/pgraphmap```

# Worker

There are two options for worker machines:

## Docker image

Simply build the image and run it (with proper environment variables setup)

## Python packages

* Install graphmap
* Install this package ```pip3 install git+https://github.com/nmiculinic/pgraphmap```
* Run (with proper environment setup) ```python -m pgraphmap.cel worker -c 1```
    * ```-c 1``` mean is accept at most one concurrent connection since graphmap parallelizes on its own.


# Usage

After insalling this package, simply run

```python3 -m pgraphmap.submit <reads.fasta> <ref.fa> <out.sam>```

```python3 -m pgraphmap.submit -h``` for help. There's not much options.  

# Cluster monitoring

This program uses celery task queue underneath the hood. Install flower ```pip install flower``` and with proper environment variables setup you could run:

```flower -A pgraphmap.cel --port=5555```

And on your localhost:5555 nice web interface shall become visible. Enjoy.
