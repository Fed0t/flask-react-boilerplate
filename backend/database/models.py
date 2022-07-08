# coding: utf-8
############################################################################################
# Models For API
#
# This file holds all of the models for the API, used by SQLALchemy to create and maintain
# the PostgreSQL DB
# https://pythonhosted.org/Flask-Security/quickstart.html
# Association Table for Roles and Users
############################################################################################
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Class to add, update and delete data via SQLALchemy sessions
class CRUD():

    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

