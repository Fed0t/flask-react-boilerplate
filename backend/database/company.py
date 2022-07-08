from marshmallow import validates
from database.validations import IS_INTEGER
from database.models import db, CRUD
from marshmallow_jsonapi import Schema, fields
from database.validations import NOT_BLANK

#CLIENT
class Company(db.Model, CRUD):
    __tablename__ = 'company'

    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String, nullable=False, unique=False)
    client_type = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship("User", foreign_keys='Company.owner_id',)
    webhook_url = db.Column(db.String, nullable=True, unique=False)
    webhook_key = db.Column(db.String, nullable=True, unique=False)
    date_updated = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, name, client_type, webhook_url, webhook_key, user_id):
        self.name = name
        self.client_type = client_type
        self.webhook_url = webhook_url
        self.webhook_key = webhook_key

    def __repr__(self):
        return '<models.company[name=%s]>' % self.name

class CompanySchema(Schema):

    # Validation for the different fields
    id           = fields.Integer(dump_only=True, required=True)
    name     = fields.String(validate=NOT_BLANK,  required=True)
    client_type = fields.Integer(validate=IS_INTEGER,  required=True)
    webhook_url = fields.String(required=False)
    webhook_key = fields.String(required=False)

    class Meta:
        type_ = 'company'

class CompanySchemaUpdate(Schema):
    # Validation for the different fields
    id           = fields.Integer(dump_only=True, required=True)
    webhook_url = fields.String(required=False)
    webhook_key = fields.String(required=False)
    class Meta:
        type_ = 'company'
