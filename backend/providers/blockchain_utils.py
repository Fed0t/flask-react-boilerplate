from jobs.send_webhook import send_webhook_to_client
from datetime import timedelta
from database.transaction import Transaction, TransactionSchema
from database.company import Company, CompanySchema
import uuid
import random

schema = TransactionSchema()
schema_client = CompanySchema()


def send_blockchain_request():
    # send and wait for blockchain modex response
    return uuid.uuid1()

def create_blockchain_transaction(transaction_id, webhooks, delay=timedelta(seconds=random.randint(10, 30))):
    transaction = Transaction.query.get(transaction_id)
    if transaction:
        blockchain_id = send_blockchain_request()
        
        transaction.blockchain_id = blockchain_id
        transaction.status = 'confirmed'

        transaction.update()
 
        transaction_query = Transaction.query.get(transaction.id)
        results = schema.dump(transaction_query)
        for webhook in webhooks:
            send_webhook_to_client(webhook[1], webhook[2], results, delay, company_id=webhook[0])


def create_blockchain_client(client_id, webhooks, delay=timedelta(seconds=10)):
    company = Company.query.get(client_id)
    if company:
        # send and wait for blockchain modex response
        company.status = 'confirmed'
        company.update()
 
        client_query = Company.query.get(company.id)
        results = schema_client.dump(client_query)
        for webhook in webhooks:
            send_webhook_to_client(webhook[0], webhook[1], results, delay, client_id=client_id)
