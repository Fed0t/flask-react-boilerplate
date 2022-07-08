from flask_pymongo import PyMongo

mongodb_client = None
db = None


def makeMongo(app):
    global mongodb_client
    global db
    mongodb_client = PyMongo(app)
    db = mongodb_client.db
