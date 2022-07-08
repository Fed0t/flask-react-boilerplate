############################################################################################
# Global Configurations - Base
#
# This file holds base global configurations for the API. In order to accomodate for
# multiple developers working on this project, this base config file is set up in order to
# have certain settings (production settings) be default. After those default settings are
# put into place, a check is made on the name of the user running the code, in the main.py
# file, and if it matches explicitly-declared users, the settings can be overridden by user-
# defined files that are housed in this same directory.
############################################################################################

from datetime import timedelta
import os

# Flask Core Settings
APP_NAME   = os.environ.get("APP_NAME", 'InvoiceCash API')
# SERVER_NAME = "invoicecash-api.dev.ro"
APP_DOMAIN = os.environ.get("APP_DOMAIN", 'localhost')
DEBUG      = os.environ.get("DEBUG")
HOST       = '0.0.0.0'
PORT       = os.environ.get("PORT", 5000)
SECRET_KEY = os.environ.get("SECRET_KEY", 'MY_SECRET_PASS')


ENABLE_ADMIN = True
ADMIN_URL = '/api/v1/admin'

#QUEUE WORKER
RQ_REDIS_URL = os.environ.get("RQ_REDIS_URL")

SWAGGER_URL = '/api/v1/docs'
SWAGGER_API_URL = '/api/v1/static/docs'
SWAGGER = {
    'title': APP_NAME + ' Documentation',
    'uiversion': 2,
    'host': APP_DOMAIN
}
# Database Settings
DB_USER = os.environ.get("DATABASE_USER")
DB_PASS = os.environ.get("DATABASE_PASS")
DB_HOST = os.environ.get("DATABASE_HOST")
DB_NAME = os.environ.get("DATABASE_NAME")

SQLALCHEMY_DATABASE_URI = 'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'.format(
                            DB_USER=DB_USER,
                            DB_PASS=DB_PASS,
                            DB_HOST=DB_HOST,
                            DB_NAME=DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = True


# Mail Settings
MAIL_SERVER   = 'smtp.mail.yahoo.com'
MAIL_PORT     = 587
MAIL_USERNAME = 'veelancing1@yahoo.com'
MAIL_PASSWORD = 'elfuvssiaqocbits'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_DEBUG = False
MAIL_DEFAULT_SENDER = MAIL_USERNAME

# Security Settings
# https://pythonhosted.org/Flask-Security/configuration.html
# https://pythonhosted.org/Flask-JWT/
JWT_MULTITOKEN_ENABLED = False
JWT_ACCESS_TOKEN_EXPIRES           = timedelta(minutes=2)
JWT_REFRESH_TOKEN_EXPIRES          = timedelta(minutes=5)
JWT_AUTH_HEADER_PREFIX         = 'Bearer'
JWT_SECRET_KEY  =  SECRET_KEY
JWT_ERROR_MESSAGE_KEY = 'error'
JWT_REFRESH_JSON_KEY = 'refresh_token'

SECURITY_CONFIRMABLE           = False
SECURITY_TRACKABLE             = True
SECURITY_REGISTERABLE          = False
SECURITY_RECOVERABLE           = False
SECURITY_PASSWORD_HASH         = 'sha512_crypt'
SECURITY_PASSWORD_SALT         = 'add_salt'

WTF_CSRF_ENABLED = False

SECURITY_FLASH_MESSAGES=False
REGISTRATION_OPEN = False