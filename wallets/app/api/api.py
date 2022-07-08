from ..wallet.configuration import Configuration
from ..tasks import makeTransaction
import json
from eth_utils.types import is_string
from flask import request
from flask_restful import Resource
from ..utils import check_payload, JSONEncoder
from ..main.database import db
from ..wallet.functions import (
    add_token,
    get_balance,
    get_wallet,
    list_tokens,
    load_wallet,
    new_wallet,
    reveal_seed,
)

keys = ["user_id", "passphrase"]
transactionKeys = ["user_id", "passphrase", "to", "amount"]
tokenKeys = ["user_id", "contract", "symbol"]
loadKeys = ["user_id", "private_key", "passphrase"]
privateKeyKeys = ["passphrase"]
slbzCommands = ["command", "params"]


class WalletView(Resource):
    def get(self, user_id):
        wallet = get_wallet(user_id)
        tokens = list_tokens(user_id)

        default_balance, default_address = get_balance(user_id=user_id)

        balance = {"ETH": {"address": default_address, "balance": str(default_balance)}}

        for token in tokens:
            b, a = get_balance(token, user_id)
            if is_string(a) and b is not None:
                balance[token] = {"address": a, "balance": str(b)}

        data = json.loads(JSONEncoder().encode(wallet))
        data["balance"] = balance

        return data


class WalletAddTokenView(Resource):
    def put(self):
        data = request.json

        if check_payload(data, tokenKeys) is False:
            return {"detail": "Error"}

        message, success = add_token(
            contract=data["contract"], symbol=data["symbol"], user_id=data["user_id"]
        )

        return {"message": message, "success": success}


class WalletAddView(Resource):
    def put(self):
        data = request.json

        if check_payload(data, keys) is False:
            return {"detail": "Error"}

        result = new_wallet(data["user_id"], data["passphrase"])
        message, success = add_token(
            contract="0x6D5bfD02b543e7D49f88Fe78628A42Ac815D46f2",
            symbol="SLBZ",
            user_id=data["user_id"],
        )

        return json.loads(JSONEncoder().encode(result))


class WalletListView(Resource):
    def get(self):

        data = db.cold_wallets.find()
        results = []

        for wallet in data:
            results.append(json.loads(JSONEncoder().encode(wallet)))

        return results


class WalletLoadView(Resource):
    def post(self):
        data = request.json

        if check_payload(data, loadKeys) is False:
            return {"detail": "Error"}

        return load_wallet(
            user_id=data["user_id"],
            private_key=data["private_key"],
            passphrase=data["passphrase"],
        )


class WalletPrivateKey(Resource):
    def post(self, user_id):
        data = request.json

        if check_payload(data, privateKeyKeys) is False:
            return {"detail": "Error"}

        return reveal_seed(user_id=user_id, password=data["passphrase"])


class TransactionAddView(Resource):
    def put(self):
        data = request.json

        if check_payload(data, transactionKeys) is False:
            return {"detail": "Error"}

        transaction = db.transactions.insert_one(
            {
                "to": data["to"],
                "status": "pending",
                "from": get_wallet(data["user_id"])["address"],
            }
        )

        makeTransaction.delay(
            to=data["to"],
            password=data["passphrase"],
            value=data["amount"],
            user_id=data["user_id"],
            token=data["token"] if "token" in data else None,
            data=data,
            t_id=str(transaction.inserted_id),
        )

        return {"detail": "Success"}


class TransactionListView(Resource):
    def get(self, wallet):
        data = db.transactions.find({"$or": [{"to": wallet}, {"from": wallet}]})
        results = []

        for transaction in data:
            t = json.loads(JSONEncoder().encode(transaction))
            t["mode"] = "out" if t["from"] == wallet else "in"
            results.append(t)

        return results
