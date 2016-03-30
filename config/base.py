import os


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    PARSE_APP_ID = os.environ.get('PARSE_APP_ID')
    PARSE_REST_API_KEY = os.environ.get('PARSE_REST_API_KEY')
    PARSE_JS_API_KEY = os.environ.get('PARSE_JS_API_KEY')
    STRIPE_KEY = os.environ.get('PENNY_STRIPE_KEY')
    REDIRECT_TO_SSL = os.environ.get('REDIRECT_TO_SSL', False)
