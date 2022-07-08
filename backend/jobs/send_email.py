from datetime import timedelta
from jobs import rq
from providers.mail_manager import mail
from flask_mail import Message

def send_email(to, subject, body):
    msg = Message(subject, recipients = [to])
    msg.body = body
    mail.send(msg)

def send_email_to_client(to, subject, body, delay = timedelta(seconds=1)):
    default_queue = rq.get_queue()
    job = default_queue.enqueue_in(delay, send_email, to, subject, body)
    return job