from datetime import timedelta
from database.transaction import Transaction
from flask_restful import Resource
from marshmallow import ValidationError
from database.order import Order, OrderSchema, db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import jsonify, request
from jobs.send_webhook import send_webhook_to_client
from providers.blockchain_utils import create_blockchain_transaction
from marshmallow_jsonapi.exceptions import IncorrectTypeError
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
# https://github.com/marshmallow-code/marshmallow-jsonapi
schema = OrderSchema(include_data=('transaction',))

class PaymentConfirm(Resource):
    def post(self):
        """
        Mobilpat payment confirm webhook
        It works also with swag_from, schemas and spec_dict
        ---
        parameters:
          - in: path
            name: username
            type: string
            required: true
        responses:
          200:
            description: A single user item
            schema:
              id: Order
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
        """
        try:
            current_user = get_jwt_identity()
            raw_dict = request.get_json(force=True)
            # Validate Data
            order_dict = schema.load(raw_dict)
            # Save the new order

            order = Order(
                order_dict.get('seller_id'), 
                order_dict.get('buyer_id'), 
                order_dict.get('order_details'),
                order_dict.get('order_type')
            )
            order.add(order)

            transaction = Transaction('pending',)
            transaction.add(transaction)

            order_query   = Order.query.get(order.id)
            order_query.transaction_id = transaction.id
            order_query.update()
            
            # Return the new order information
            results = schema.dump(order_query)
            webhooks = [
                (order_query.buyer.id, order_query.buyer.webhook_url, order_query.buyer.webhook_key), 
                (order_query.seller.id, order_query.seller.webhook_url, order_query.seller.webhook_key)
            ]

            # Queue job where we will save the modex transaction_id
            create_blockchain_transaction(transaction.id, webhooks)

            for webhook in webhooks:
                send_webhook_to_client(
                    webhook_url=webhook[1], 
                    webhook_key=webhook[2], 
                    payload=results, 
                    delay=timedelta(seconds=1), 
                    client_id=webhook[0]
                )

            return results, 201

        except ValidationError as err:
            resp = jsonify(err.messages)
            resp.status_code = 403
            return resp
            
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            if isinstance(e, IntegrityError):
                resp = jsonify({"error": 'Integrity error.'})
            return resp
        
        except IncorrectTypeError as e:
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp
