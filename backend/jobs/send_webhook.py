from requests.exceptions import ConnectionError, Timeout, RetryError, HTTPError, RequestException
from database.webhook import Webhook
from requests import Session
from datetime import timedelta
from json.decoder import JSONDecodeError
from rq import Retry
import json
from jobs import rq

def request_http_instance():
    return Session()

def send_request(webhook_url, webhook_key = '', payload = {}, company_id = None):
    session = request_http_instance()
    headers = {
        'Authorization': 'Bearer ' + str(webhook_key),
        'Content-Type': 'application/json'
    }
    send_payload = json.dumps(payload, indent=4)
    response = session.post(webhook_url, data = send_payload, headers=headers)

    try:
        response.raise_for_status()
        jsonResponse = json.loads(response.text)
    except (HTTPError, ConnectionError, Timeout, RequestException, RetryError, JSONDecodeError) as http_error:
        jsonResponse = {'error': str(http_error)}

    webhook_log = Webhook(company_id, response.status_code, json.dumps(jsonResponse), )
    webhook_log.add(webhook_log)

    if 'error' in jsonResponse:
        raise BaseException(jsonResponse['error'])



def send_webhook_to_client(webhook_url, webhook_key, payload , delay = timedelta(seconds=1), company_id = None):
    default_queue = rq.get_queue()
    if webhook_url and len(webhook_url) > 0:
        job = default_queue.enqueue_in(delay, send_request, webhook_url, webhook_key, payload, company_id, retry=Retry(max=2, interval=15))
        return job