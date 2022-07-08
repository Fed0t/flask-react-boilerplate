import json
from bson.objectid import ObjectId
from ..main.database import db
from ..main.worker import celery
from ..utils import JSONEncoder


@celery.task(name="wallet.transaction")
def makeTransaction(to, password, value, user_id, token, data, t_id):
    from ..wallet.functions import (
        get_wallet,
        send_transaction,
    )

    data_transaction = send_transaction(to, value, user_id, password, token)
    transaction_data = db.transactions.find_one({"_id": ObjectId(t_id)})
    transaction_data = json.loads(JSONEncoder().encode(transaction_data))
    transaction_data.__delitem__("_id")

    if "detail" in data_transaction:
        transaction_data.__setitem__("status", "rejected")
        transaction_data.__setitem__("amount", data["amount"])
        transaction_data.__setitem__("cause", data_transaction["detail"])
        db.transactions.update_one({"_id": ObjectId(t_id)}, {"$set": transaction_data})
        return

    for key in data_transaction.keys():
        transaction_data.__setitem__(key, data_transaction[key])

    transaction_data.__setitem__("amount", data["amount"])
    transaction_data.__setitem__("to", data["to"])
    transaction_data.__setitem__("from", get_wallet(data["user_id"])["address"])
    transaction_data.__setitem__("cost", data_transaction["cost"])
    transaction_data.__setitem__("status", "complete")

    db.transactions.update_one({"_id": ObjectId(t_id)}, {"$set": transaction_data})
