import json

from flask import Flask
from flask.ext.testing import TestCase

from app_init import init


class BaseTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        init(app, 'ut')

        self.test_client = app.test_client()
        self.config = app.config
        self.app = app
        app.config['SECRET_KEY'] = 'test_secret_key'

        return app

    def get_json(self, url):
        response = self.test_client.get(url)
        self.assertEqual(response.content_type, 'application/json')
        return json.loads(response.data), response.status_code

    def put_json(self, url, data):
        response = self.test_client.put(
            url,
            data=json.dumps(data),
            content_type='application/json')
        self.assertEqual(response.content_type, 'application/json')
        return json.loads(response.data), response.status_code

    def post_json(self, url, data):
        response = self.test_client.post(
            url,
            data=json.dumps(data),
            content_type='application/json')
        self.assertEqual(response.content_type, 'application/json')
        return json.loads(response.data), response.status_code

    def delete_json(self, url):
        response = self.test_client.delete(url)
        self.assertEqual(response.content_type, 'application/json')
        return json.loads(response.data), response.status_code
