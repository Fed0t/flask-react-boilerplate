
from database.models import db, CRUD
from marshmallow_jsonapi import Schema, fields
from datetime import timezone, datetime
from flask_jwt_extended import decode_token
from flask_jwt_extended.exceptions import RevokedTokenError
from sqlalchemy import desc
from flask import current_app

class TokenBlocklist(db.Model, CRUD):
    __tablename__ = 'token_blocklist'
    id = db.Column(db.Integer, primary_key=True)
    token_id = db.Column(db.Integer, db.ForeignKey('token.id'))
    created_at = db.Column(db.DateTime, nullable=False)

class Token(db.Model, CRUD):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    jti = db.Column(db.String(120), nullable=True)
    access_token = db.Column(db.Text(), nullable=False, index=False)
    refresh_token = db.Column(db.Text(), nullable=False, index=False)
    created_at = db.Column(db.DateTime, nullable=False)


    def add_current_token_to_blocklist(self, user_id):
        if current_app.config['JWT_MULTITOKEN_ENABLED'] is False:
            token = db.session.query(Token).filter_by(user_id=user_id).order_by(desc('id')).first()
            if token:
                token_blocklist = TokenBlocklist.query.filter_by(token_id=token.id).first()
                if token_blocklist is None:
                    now = datetime.now(timezone.utc)
                    db.session.add(TokenBlocklist(token_id = token.id, created_at=now))
                    db.session.commit()

    def check_if_token_is_blocked(self, user_id, jti):
        token = db.session.query(Token).filter_by(user_id=user_id, jti=jti).order_by(desc('created_at')).first()
        if token:
            token_blocklist = TokenBlocklist.query.filter_by(token_id=token.id).first()
            if token_blocklist is not None:
               return True
