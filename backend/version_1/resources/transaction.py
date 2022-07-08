from flask_restful import Resource
from marshmallow import ValidationError
from database.transaction import Transaction, TransactionSchema, db
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify, request
from flask_jwt_extended import jwt_required

# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
# https://github.com/marshmallow-code/marshmallow-jsonapi
schema = TransactionSchema()

class TransactionBlockchainWebhook(Resource):
    # @jwt_required()
    def post(self):
        '''
        http://jsonapi.org/format/#crud
        A resource can be created by sending a POST request to a URL that represents a collection of resources.
        The request MUST include a single resource object as primary data. The resource object MUST contain at
        least a type member.

        If a POST request did not include a Client-Generated ID and the requested resource has been created
        successfully, the server MUST return a 201 Created status code
        '''

        try:
            raw_dict = request.get_json(force=True)
            transaction_dict = schema.load(raw_dict)
            transaction = Transaction.query.get(transaction_dict['id'])

            if transaction:
                for key, value in transaction_dict.items():
                    setattr(transaction, key, value)
                transaction.update()
            else:
                resp = jsonify({"error": "Transaction not found"})
                resp.status_code = 404
                return resp

            transaction = Transaction.query.get(transaction.id)
            results = schema.dump(transaction)
        
            return results, 201

        except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 401
                return resp

        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp


class TransactionList(Resource):
    @jwt_required()
    def get(self):
        '''
        http://jsonapi.org/format/#fetching
        A server MUST respond to a successful request to fetch an individual resource or resource collection
        with a 200 OK response.

        A server MUST respond with 404 Not Found when processing a request to fetch a single resource that
        does not exist, except when the request warrants a 200 OK response with null as the primary data
        (as described above) a self link as part of the top-level links object
        '''
        transactions_query = Transaction.query.all()
        results    = schema.dump(transactions_query, many=True)
        return results


class TransactionShow(Resource):
    @jwt_required()
    def get(self, id):
        '''
        http://jsonapi.org/format/#fetching
        A server MUST respond to a successful request to fetch an individual resource or resource collection with
        a 200 OK response.

        A server MUST respond with 404 Not Found when processing a request to fetch a single resource that does not
        exist, except when the request warrants a 200 OK response with null as the primary data (as described above)
        a self link as part of the top-level links object
        '''
        transaction_query = Transaction.query.get_or_404(id)
        result    = schema.dump(transaction_query)
        return result

