from bootstrap import init_app, db
from jobs import rq
from redis import Redis
import sys
sys.tracebacklimit = 0

app = init_app()

if __name__ == '__main__':
    default_worker = rq.get_worker()
    default_worker.work(with_scheduler=True)
