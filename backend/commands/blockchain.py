import click
from flask.cli import AppGroup
from packages.modex_client import Authorization

blockchain = AppGroup('blockchain', short_help="Perform blockchain operations")

@blockchain.command('ping')
@click.argument('new_token')
def ping(host):
    """Generate a new token """

    auth = Authorization()
    auth.generate_token()
    print("We trying to get new token : {}".format(host))

