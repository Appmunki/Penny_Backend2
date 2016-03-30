import sys
from flask import logging
from flask_sslify import SSLify

from parse_rest.connection import register

import stripe

from app.common.resources import logger

from config import routes
from shared.resources import db


class Initializer(object):
    def __init__(self, app, env_name):
        self.app = app
        self.env_name = env_name

    def init_db(self):
        db.init_app(self.app)

    def init_routes(self):
        routes.init_app(self.app)

    def get_config_object_name(self, env_name):
        return 'config.{}.Config'.format(env_name)

    def init_config(self):
        config_name = self.get_config_object_name(self.env_name)
        self.app.config.from_object(config_name)
        self.app.config['ENV'] = self.env_name

    def init_parse(self):
        parse_app_id = self.app.config['PARSE_APP_ID']
        parse_rest_api_key = self.app.config['PARSE_REST_API_KEY']

        if parse_app_id is None or parse_rest_api_key is None:
            logger.critical('parse_app_id and rest_api cannot be null')
            sys.exit(-1)
        register(parse_app_id, parse_rest_api_key)

    def init_stripe(self):
        if self.app.config['STRIPE_KEY'] is None:
            logger.critical('stripe_key cannot be null')
            sys.exit(-1)
        stripe.api_key = self.app.config['STRIPE_KEY']

    def init_logging(self):
        self.app.logger.addHandler(logging.StreamHandler(sys.stdout))
        self.app.logger.setLevel(logging.DEBUG)
        logger.set_logger(self.app.logger)


def init(app, env_name=None):
    if env_name is None:
        env_name = 'dev'
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

    initializer = Initializer(app, env_name)
    initializer.init_config()
    initializer.init_routes()
    initializer.init_parse()
    initializer.init_stripe()
    initializer.init_logging()

    if app.config.get('REDIRECT_TO_SSL'):
        SSLify(app=app)
    logger.info('Initialized app with config for env: {}'.format(env_name))
