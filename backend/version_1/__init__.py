from flask_cors import CORS
from flask_restful import Api
from flask import current_app
from flask import Blueprint, request, render_template
from version_1.resources.client import ClientCreate, ClientUpdate
from version_1.resources.order import OrderCreate
from version_1.resources.transaction import TransactionBlockchainWebhook
from version_1.resources.user import UserLogin, RefreshToken, LogoutUser
# from version_1.resources.role import RoleList, RoleUpdate
# from version_1.resources.user import UserList, UserUpdate

v1 = Blueprint('v1', __name__)
CORS(v1)


api = Api()
api.init_app(v1)

@v1.route('/' , methods=['GET'])
def homepage():
    return render_template('homepage.html', text=current_app.config['APP_NAME'])

@v1.route('/client-webhook-1' , methods=['POST'])
def show():
    try:
        raw_dict = request.get_json(force=True)
    except:
        raw_dict = {}
    return raw_dict, 201

#############################################
########## Resources to Add to Api
#############################################
# Set up the API and init the blueprint

api.add_resource(UserLogin, '/login')
api.add_resource(LogoutUser, '/logout')
api.add_resource(RefreshToken, '/token/refresh')
api.add_resource(OrderCreate, '/orders')
# api.add_resource(ClientCreate, '/companies')
# api.add_resource(ClientUpdate, '/companies/<int:id>')
# Transactions (Get transaction id)
# api.add_resource(TransactionShow, '/transactions/<int:id>')
# Transactions Webhooks (Modex Webhook to update transaction)
api.add_resource(TransactionBlockchainWebhook, '/webhooks/modex')

# api.add_resource(UserRegister, '/auth/register')
# api.add_resource(UserUpdate, '/users/<int:id>')
# # Roles
# api.add_resource(RoleList, '/roles')
# api.add_resource(RoleUpdate, '/roles/<int:id>')
