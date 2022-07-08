import sys
sys.tracebacklimit = 0
from redis import Redis
from jobs import rq
from bootstrap import init_app, db

app = init_app()

if __name__ == '__main__':
    default_worker = rq.get_worker()
    default_worker.work(with_scheduler=True)
