from app.main.celery import make_celery
from app.main.database import makeMongo
from flask import Flask
from flask_restful import Api
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# # Sentry Bug Tracker
# sentry_sdk.init(
#     dsn="https://4d2effb3a9304c3c8e8d149f094a9e02@o877381.ingest.sentry.io/5828060",
#     integrations=[FlaskIntegration()],
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0,
# )

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://192.168.1.204:27017/netopia_wallets_db"
app.config["CELERY_RESULT_BACKEND"] = "mongodb://192.168.1.204:27017/jobs"
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/0"


# @app.route("/debug-sentry")
# def trigger_error():
#     division_by_zero = 1 / 0


api = Api(app)
celery = make_celery(app)

makeMongo(app)


from ..api.api import (
    TransactionAddView,
    TransactionListView,
    WalletAddTokenView,
    WalletAddView,
    WalletListView,
    WalletLoadView,
    WalletPrivateKey,
    WalletView,
)

api.add_resource(TransactionListView, "/transactions/<string:wallet>")
api.add_resource(TransactionAddView, "/transaction/")
api.add_resource(WalletListView, "/wallets")
api.add_resource(WalletAddView, "/wallets/")
api.add_resource(WalletLoadView, "/wallet/load/")
api.add_resource(WalletAddTokenView, "/wallet/token/")
api.add_resource(WalletView, "/wallet/<int:user_id>")
api.add_resource(WalletPrivateKey, "/wallet/<int:user_id>/seed")


if __name__ == "__main__":
    app.run(debug=True)
