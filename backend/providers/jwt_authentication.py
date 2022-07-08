
############################################################################################
# JWT Functions for Authenticating Users via API
############################################################################################
# https://github.com/rohitchormale/flask-examples/blob/master/flask-security-with-flask-jwt-extended-example.py

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from database import user_datastore, TokenBlocklist, db, Token
from flask_security.utils import verify_password
from flask_security.forms import RegisterForm, ConfirmRegisterForm, LoginForm
from flask_security import current_user

jwt_manager = JWTManager()

# https://github.com/graup/flask-restless-security/blob/master/server.py
def authenticate_flask_security(username, password):
    try:
        user = user_datastore.find_user(email=username)
    except KeyError:
        return None
    if username == user.email and verify_password(password, user.password):
        return user
    return None

def load_user(payload):
    user = user_datastore.find_user(id=payload['identity'])
    return user



# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
# @jwt_manager.user_identity_loader
# def user_identity_lookup(user):
#     return user.id


# # Register a callback function that loads a user from your database whenever
# # a protected route is accessed. This should return any python object on a
# # successful lookup, or None if the lookup failed for any reason (for example
# # if the user has been deleted from the database).
# @jwt_manager.user_lookup_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     identity = jwt_data["sub"]
#     return User.query.filter_by(id=identity).one_or_none()
