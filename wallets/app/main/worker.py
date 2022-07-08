from app.main.celery import make_celery
from app.main.database import makeMongo
from flask import Flask


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://192.168.1.204:27017/netopia_wallets_db"
app.config["CELERY_RESULT_BACKEND"] = "mongodb://192.168.1.204:27017/jobs"
app.config["CELERY_BROKER_URL"] = "redis://192.168.1.177:6379/0"

makeMongo(app)

celery = make_celery(app)
