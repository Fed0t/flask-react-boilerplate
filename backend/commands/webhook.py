import click
from flask.cli import AppGroup
from packages.modex_client import Authorization

blockchain = AppGroup('webhook', short_help="Perform webhook operations")

@blockchain.command('listen')
def ping(host):
    """Wait for webhooks """

    auth = Authorization()
    auth.generate_token()
    print("We trying to get new token : {}".format(host))

