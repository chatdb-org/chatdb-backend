""" This file contains the configuration variables for the app. """

# pylint: disable=import-error
from decouple import config

db_user = config('DB_USER', de)
db_password = config('DB_PASSWORD')
db_host = config('DB_HOST')
db_port = config('DB_PORT')
db_name = config('DB_NAME')
environment = config('ENVIRONMENT')
openai_key = config('OPENAI_KEY')
