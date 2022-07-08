from database.models import db, CRUD

#Webhooks
class Webhook(db.Model, CRUD):
    __tablename__ = 'webhook'

    id  = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    response_code = db.Column(db.Integer, nullable=True, unique=False)
    response_data = db.Column(db.String, nullable=True, unique=False)

    date_created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, company_id, response_code, response_data):
        self.company_id = company_id
        self.response_code = response_code
        self.response_data = response_data

    def __repr__(self):
        return '<models.webhook[client_id=%s]>' % self.company_id
