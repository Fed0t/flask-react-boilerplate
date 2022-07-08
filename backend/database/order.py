
from database.models import db, CRUD
from marshmallow_jsonapi import Schema, fields
from database.validations import NOT_BLANK, IS_INTEGER

#ORDER
class Order(db.Model, CRUD):
    __tablename__ = 'order'

    id           = db.Column(db.Integer, primary_key=True)
    order_type     = db.Column(db.String, nullable=False, unique=False)
    order_details = db.Column(db.String, nullable=True, unique=False, default="")
    
    buyer_id     = db.Column(db.Integer, db.ForeignKey('company.id'))
    seller_id     = db.Column(db.Integer, db.ForeignKey('company.id'))

    buyer =  db.relationship("Company", foreign_keys='Order.buyer_id',)
    seller = db.relationship("Company", foreign_keys='Order.seller_id',)

    owner =   db.Column(db.Integer, db.ForeignKey('user.id'))

    transactions  = db.relationship('Transaction', backref=db.backref('orders'))

    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, buyer_id, seller_id, order_details, order_type, user_id):
        self.order_details = order_details
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.order_type = order_type
        self.owner = user_id
        
    def __repr__(self):
        return '<models.order[order_type=%s]>' % self.order_type


class OrderSchema(Schema):
    id           = fields.Integer(dump_only=True)
    order_type     = fields.String(validate=NOT_BLANK, required=True)
    order_details  = fields.String(validate=NOT_BLANK, required=True)
    seller_id = fields.Integer(validate=IS_INTEGER, required=True)
    buyer_id = fields.Integer(validate=IS_INTEGER, required=True)
    transaction_id = fields.String(required=False)

    transaction = fields.Relationship(
                                many=False,
                                include_resource_linkage=False,
                                type_='transaction',
                                schema='TransactionSchema'
    )

    date_created = fields.DateTime(dump_only=True)

    class Meta:
        strict = True
        type_ = 'order'
