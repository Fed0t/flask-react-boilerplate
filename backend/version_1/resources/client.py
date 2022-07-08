from flask_restful import Resource
from flask import jsonify, request
from database import Company, CompanySchema, CompanySchemaUpdate, db
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from datetime import timedelta
from marshmallow_jsonapi.exceptions import IncorrectTypeError
from providers.blockchain_utils import create_blockchain_client
from jobs.send_email import send_email_to_client
from flask_jwt_extended import jwt_required, get_jwt_identity
# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
# https://github.com/marshmallow-code/marshmallow-jsonapi
schema = CompanySchema()
schema_update = CompanySchemaUpdate()

class ClientCreate(Resource):
    @jwt_required()
    def post(self):
        """
        Colors API using schema
        This example is using marshmallow schemas
        """
        '''
        http://jsonapi.org/format/#fetching
        A server MUST respond to a successful request to fetch an individual resource or resource collection with
        a 200 OK response.

        A server MUST respond with 404 Not Found when processing a request to fetch a single resource that does not
        exist, except when the request warrants a 200 OK response with null as the primary data (as described above)
        a self link as part of the top-level links object
        '''
     
        try:
            raw_dict = request.get_json(force=True)
            current_user = get_jwt_identity()
            # Validate Data
            client_dict = schema.load(raw_dict)
            
            # Save the new order
            client = Company(
                client_dict.get('name'), 
                client_dict.get('client_type'), 
                client_dict.get('webhook_url'),
                client_dict.get('webhook_key'),
                user_id=current_user.id
            )
            client.add(client)
            # Return the new client information
            query   = Company.query.get(client.id)
            results = schema.dump(query)

            # Send request to modex-blockchain
            create_blockchain_client(client.id, webhooks=[(query.webhook_url, query.webhook_key)])

            return results, 201

        except ValidationError as err:
            resp = jsonify(err.messages)
            resp.status_code = 403
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp

        except IncorrectTypeError as e:
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp

class ClientUpdate(Resource):
    @jwt_required()
    def patch(self, id):
        '''
        http://jsonapi.org/format/#fetching
        A server MUST respond to a successful request to fetch an individual resource or resource collection with
        a 200 OK response.

        A server MUST respond with 404 Not Found when processing a request to fetch a single resource that does not
        exist, except when the request warrants a 200 OK response with null as the primary data (as described above)
        a self link as part of the top-level links object
        '''

        try:
            raw_dict = request.get_json(force=True)
            client_dict = schema_update.load(raw_dict)
            client   = Company.query.get(id)
            if client:
                for key, value in client_dict.items():
                    setattr(client, key, value)
                db.session.commit()
            else:
                resp = jsonify({"error": "Client not found"})
                resp.status_code = 404
                return resp
                
            query_client   = Company.query.get(id)
            create_blockchain_client(
                query_client.id, 
                webhooks=[(query_client.webhook_url, query_client.webhook_key)], 
                delay=timedelta(seconds=1)
            )

            send_email_to_client(
                query_client.email, 
                'Your account was updated', 
                'You updated your account successfully.'
            )
            results = schema_update.dump(query_client)
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

