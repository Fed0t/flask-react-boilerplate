from database.models import db, CRUD
from marshmallow_jsonapi import Schema, fields
from database.validations import NOT_BLANK

#TRANSACTIONS
class Transaction(db.Model, CRUD):
    __tablename__ = 'transaction'

    id           = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    status = db.Column(db.String, nullable=False, unique=False)
    blockchain_id = db.Column(db.String, nullable=True, unique=True) #modex id
    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, status):
        self.status = status

    def __repr__(self):
        return '<models.transaction[blockchain_id=%s]>' % self.blockchain_id

class TransactionSchema(Schema):

    # Validation for the different fields
    id           = fields.Integer(dump_only=True)
    blockchain_id = fields.String(required=False)
    status = fields.String(validate=NOT_BLANK)
    date_created = fields.DateTime(dump_only=True)
    class Meta:
        type_ = 'transaction'
