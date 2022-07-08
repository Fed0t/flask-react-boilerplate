webhook_groups = {
    'blockchain' : {
        'endpoint' : '/webhooks/transactions',
        'method' : 'POST',
        'callback' : 'transaction_blockchain_webhook'
    },
    'stripe'  : {
        'endpoint' : '/webhooks/stripe',
        'method' : 'POST',
        'callback' : 'transaction_blockchain_webhook'
    },
}

