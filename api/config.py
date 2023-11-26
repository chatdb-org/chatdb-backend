""" This file contains the configuration variables for the app. """

# pylint: disable=import-error
from decouple import config

db_user = config('DB_USER', default=None)
db_password = config('DB_PASSWORD', default=None)
db_host = config('DB_HOST', default=None)
db_port = config('DB_PORT', default=None)
db_name = config('DB_NAME', default=None)
environment = config('ENVIRONMENT', default='development')
openai_key = config('OPENAI_KEY', default=None)
