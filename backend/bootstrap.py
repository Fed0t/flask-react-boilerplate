#!/usr/bin/env python3
############################################################################################
# Main Processing of App
#
# This file is the meat of the API. The app is initialized, DB is accessed, and config files
# are loaded up. Note that it is in this file that user-defined config files are chosen,
# if they exist.
############################################################################################
from flask import Flask
from jobs import rq
from version_1 import v1
from dotenv import load_dotenv
from providers.schema_manager import marshmallow
from providers.mail_manager import mail
from providers.migration_manger import migrate
from providers.jwt_authentication import jwt_manager
from providers.swagger_docs import swagger
from providers.security_manager import security
from werkzeug.middleware.proxy_fix import ProxyFix
from database import User, Role, Order, Transaction, Company, Webhook, db, user_datastore, Token, TokenBlocklist
from database.fresh_data import create_models
from commands import init_commands

########## Bootstrap Application ##########
def init_app():
    load_dotenv()
    app = Flask(__name__, static_folder=None)
    app.config.from_object('config.settings')
    db.init_app(app)
    mail.init_app(app)
    marshmallow.init_app(app)
    migrate.init_app(app, db)
    rq.init_app(app)
    security.init_app(app, user_datastore, register_blueprint=False)
    jwt_manager.init_app(app)
    app.register_blueprint(v1, url_prefix='/api/v1')
    swagger.init_app(app)
    init_commands(app)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    if app.config['ENABLE_ADMIN']:
        from providers.admin_manager import admin_ui
        admin_ui.init_app(app)
    # Callback function to check if a JWT exists in the database blocklist
    @jwt_manager.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        current_user = user_datastore.find_user(email=jwt_payload['sub'])
        blocked = Token().check_if_token_is_blocked(user_id=current_user.id, jti=jwt_payload['jti'])

        return blocked is not None

    @app.before_first_request
    def bootstrap_app():
        if db.session.query(User).count() == 0:
            create_models()

    @app.shell_context_processor
    def make_shell_context():
        return dict(app=app, db=db, User=User, Order=Order, Role=Role,
                    Transaction=Transaction, Company=Company, Webhook=Webhook)

    return app