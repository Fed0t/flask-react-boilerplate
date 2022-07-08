from operator import truediv
from flask_restful import Resource
from datetime import datetime, timedelta, timezone
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from flask_security.utils import encrypt_password
from flask import jsonify, make_response, request, abort
from database import TokenBlocklist, UserSchema, db, user_datastore, Token
from flask_security.utils import login_user
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, unset_jwt_cookies, decode_token
from providers.jwt_authentication import authenticate_flask_security, jwt_manager

# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
# https://github.com/marshmallow-code/marshmallow-jsonapi
schema = UserSchema()
now = datetime.now(timezone.utc)

class LogoutUser(Resource):
    @jwt_required()
    def post(self):
        """
        This is endpoint to logout
        ---
        parameters:
          - in: path
        responses:
          200:
            description: Revoke the current token
        """
        try:
            current_user = get_jwt_identity()
            token = Token.query.filter_by(user_id=current_user.id).first()
            if token:
                Token().add_to_blocklist(user_id=current_user.id)
                unset_jwt_cookies(current_user)
                return jsonify(msg="JWT revoked")
            return jsonify(msg="Token not found")


        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp

class UserLogin(Resource):
    def post(self):
        """
        This is endpoint to generate a token with
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
              id: User
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
        """
        try:
            raw_dict = request.get_json(force=True)
            # Activate the User
            user = user_datastore.find_user(email=raw_dict['email'])
            if authenticate_flask_security(raw_dict['email'], raw_dict['password']):
                login_user(user)
                access_token = create_access_token(identity=user.email)
                refresh_token = create_refresh_token(identity=user.email)
                decoded_jwt = decode_token(access_token)
                Token().add_current_token_to_blocklist(user_id=user.id)
                db.session.add(
                    Token(
                        access_token=access_token, 
                        refresh_token=refresh_token, 
                        created_at=now, 
                        jti=decoded_jwt['jti'], 
                        user_id=user.id
                    ))
                db.session.commit()
                # Return new user information
                results = schema.dump(user)
                results['data']['token'] = access_token
                results['data']['refresh_token'] = refresh_token
                return results, 201

            return jsonify(msg="Invalid credentials")

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp

class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        This is endpoint to refresh token with
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
              id: User
              properties:
                username:
                  type: string
                  description: The name of the user
                  default: Steven Wilson
        """
        try:
            identity = get_jwt_identity()
            access_token = create_access_token(identity=identity)
            return jsonify(access_token=access_token), 201

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp


class UserRegister(Resource):
    def post(self):
        '''
        http://jsonapi.org/format/#crud
        A resource can be created by sending a POST request to a URL that represents a collection of resources.
        The request MUST include a single resource object as primary data. The resource object MUST contain at
        least a type member.

        If a POST request did not include a Client-Generated ID and the requested resource has been created
        successfully, the server MUST return a 201 Created status code
        '''
        raw_dict = request.get_json(force=True)
        try:
            # Validate Data
            schema.validate(raw_dict)

            # Save the new user
            user_dict = raw_dict['data']['attributes']
            user_datastore.create_user(email=user_dict['email'],
                                    password=encrypt_password(user_dict['password']),
                                    first_name=user_dict['first_name'],
                                    last_name=user_dict['last_name'],
            )

            db.session.commit()

            # Activate the User
            user = user_datastore.find_user(email=user_dict['email'])
            user_datastore.activate_user(user)

            # Return new user information
            results = schema.dump(user).data
            return results, 201

        except ValidationError as err:
            resp = jsonify({"error": err.messages})
            resp.status_code = 403
            return resp

        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            resp.status_code = 403
            return resp


class UserUpdate(Resource):
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
        try:
            user_query = user_datastore.find_user(id=id)
            result     = schema.dump(user_query)
            return result
        except KeyError as err:
            abort(404)

    @jwt_required()
    def patch(self, id):
        '''
        http://jsonapi.org/format/#crud-updating
        The PATCH request MUST include a single resource object as primary data. The resource object MUST contain
        type and id members.

        If a request does not include all of the attributes for a resource, the server MUST interpret the missing
        attributes as if they were included with their current values. The server MUST NOT interpret missing
        attributes as null values.

        If a server accepts an update but also changes the resource(s) in ways other than those specified by the
        request (for example, updating the updated-at attribute or a computed sha), it MUST return a 200 OK
        response. The response document MUST include a representation of the updated resource(s) as if a GET request was made to the request URL.

        A server MUST return 404 Not Found when processing a request to modify a resource that does not exist.
        '''
        try:
            user      = user_datastore.find_user(id=id)
        except KeyError as err:
            abort(404)

        raw_dict = request.get_json(force=True)

        try:
            schema.validate(raw_dict)
            user_dict = raw_dict['data']['attributes']
            for key, value in user_dict.items():
                setattr(user, key, value)

            db.session.commit()
            return self.get(id)

        except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 401
                return resp

        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp

    @jwt_required()
    def delete(self, id):
        '''
        http://jsonapi.org/format/#crud-deleting
        A server MUST return a 204 No Content status code if a deletion request is successful and no content is returned.
        '''
        try:
            user      = user_datastore.find_user(id=id)
        except KeyError as err:
            abort(404)
        try:
            delete = user_datastore.delete_user(user)
            db.session.commit()
            response             = make_response()
            response.status_code = 204
            return response

        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp
