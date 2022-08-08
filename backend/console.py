############################################################################################
# Migrate script
#
# This file is necessary to initialize and keep track of database migrations.
############################################################################################
from main import app
from flask.cli import FlaskGroup

cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
