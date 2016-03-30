import json

import requests


class HttpClient(object):
    def __init__(self, uri=None, headers=None):
        self.uri = uri
        if headers is None:
            headers = {}
        self.headers = headers

        headers.update({
            'Content-Type': 'application/json'
        })

    def http_request(self, method, path, params=None, body=None, headers=None):
        url = self.uri + path

        if body is not None:
            body = json.dumps(body)
        response = getattr(requests, method)(
            url,
            headers=headers or self.headers,
            params=params,
            data=body)

        response.raise_for_status()

        return self.content_from_response(response)

    def content_from_response(self, response):
        return response.text

    def get(self, path, params=None, body=None, headers=None):
        return self.http_request('get', path, params, body, headers)

    def post(self, path, params=None, body=None, headers=None):
        return self.http_request('post', path, params, body, headers)

    def delete(self, path, params=None, body=None, headers=None):
        return self.http_request('delete', path, params, body, headers)

    def put(self, path, params=None, body=None, headers=None):
        return self.http_request('put', path, params, body, headers)
