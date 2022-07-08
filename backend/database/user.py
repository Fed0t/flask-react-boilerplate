from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from database.models import db
from marshmallow_jsonapi import Schema, fields
from database.validations import NOT_BLANK, PASSWORD_LENGTH
from sqlalchemy.orm import validates
from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore
from hmac import compare_digest

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

companies_users = db.Table('companies_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('company_id', db.Integer(), db.ForeignKey('company.id')))

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id               = db.Column(db.Integer, primary_key=True)
    email            = db.Column(db.String(255), unique=True)
    password         = db.Column(db.String(255))
    first_name       = db.Column(db.String(255))
    last_name        = db.Column(db.String(255))
    active           = db.Column(db.Boolean())
    confirmed_at     = db.Column(db.DateTime())
    last_login_at    = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip    = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count      = db.Column(db.Integer())

    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    companies = db.relationship('Company', secondary=companies_users, backref=db.backref('users',  lazy='dynamic') )
    orders  = db.relationship('Order', backref=db.backref('users'))
    tokens  = db.relationship('Token', backref=db.backref('users'))

    def check_password(self, password):
        return compare_digest(password, "password")

    # http://docs.sqlalchemy.org/en/rel_1_0/orm/mapped_attributes.html#simple-validators
    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address
        return address

    def __repr__(self):
        return '<models.User[email=%s]>' % self.email

class UserSchema(Schema):

    # Validation for the different fields
    id               = fields.Integer(dump_only=True)
    email            = fields.String(validate=NOT_BLANK)
    password         = fields.String(load_only=True, validate=PASSWORD_LENGTH)
    first_name       = fields.String(validate=NOT_BLANK)
    last_name        = fields.String(validate=NOT_BLANK)
    active           = fields.Boolean(dump_only=True)
    confirmed_at     = fields.DateTime(dump_only=True)
    last_login_at    = fields.DateTime(dump_only=True)
    current_login_at = fields.DateTime(dump_only=True)
    last_login_ip    = fields.String(dump_only=True)
    current_login_ip = fields.String(dump_only=True)
    login_count      = fields.Integer(dump_only=True)

    roles = fields.Relationship(many=True,
                                include_resource_linkage=True,
                                type_='role',
                                schema='RoleSchema',
                                # related_url='/roles/{role_id}',
                                # related_url_kwargs={'role_id': '<role.id>'}
    )
    orders  = fields.Relationship(many=True,
                                include_resource_linkage=True,
                                type_='order',
                                schema='OrderSchema',
                                # related_url='/order/{order_id}',
                                # related_url_kwargs={'order_id': '<order.id>'}
    )

    # Self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/users/"
        else:
            self_link = "/users/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'user'




class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id          = db.Column(db.Integer(), primary_key=True)
    name        = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<models.Role[name=%s]>' % self.name

class RoleSchema(Schema):

    # Validates for the different fields
    id          = fields.Integer(dump_only=True)
    name        = fields.String(validate=NOT_BLANK)
    description = fields.String(validate=NOT_BLANK)

    # Self links
    def get_top_level_links(self, data, many):
        if data:
            if many:
                self_link = "/roles/"
            else:
                self_link = "/roles/{}".format(data['id'])
            return {'self': self_link}

    class Meta:
        type_ = 'role'


# https://pythonhosted.org/Flask-Security/quickstart.html
user_datastore = SQLAlchemyUserDatastore(db, User, Role)



