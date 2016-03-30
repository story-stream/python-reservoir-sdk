import json
import requests

from constants import ARGUMENT_CONVERTED_KEY, DEFAULT_BASE_URL
from errors import (
    ForbiddenError,
    ResponseError,
    NotFoundError,
    InvalidAccessTokenError,
    RateLimitExceededError,
    UnauthorizedError
)
from models import GenericModel
from utils import ArgumentConverter


class Client(object):
    """
    A client for the Reservoir API.
    """

    def __init__(self, access_token=None, base_url=None):
        self._access_token = access_token
        self._base_url = base_url or DEFAULT_BASE_URL
        self._argument_converter = ArgumentConverter()

    def get(self, path, **kwargs):
        return self._request('get', path, **kwargs)

    def post(self, path, **kwargs):
        post_data = kwargs.copy()

        if 'data' not in post_data:
            post_data = {
                'data': kwargs
            }

        return self._request('post', path, **post_data)

    def put(self, path, **kwargs):
        post_data = kwargs.copy()

        if 'data' not in post_data:
            post_data = {
                'data': kwargs
            }

        return self._request('put', path, **post_data)

    def delete(self, path, **kwargs):
        return self._request('delete', path, **kwargs)

    def _request(self, method, path, **kwargs):
        params = kwargs.copy()

        if method != 'get':
            data = params.get('data')
            if data:
                del params['data']
        else:
            data = params

        if not data.get(ARGUMENT_CONVERTED_KEY):
            data = self._argument_converter(**data)

        if ARGUMENT_CONVERTED_KEY in data:
            del data[ARGUMENT_CONVERTED_KEY]

        response = requests.request(
            method=method,
            url=self._build_url(path),
            headers=self._build_headers(),
            json=data
        )
        return self._parse_response(response)

    def _build_url(self, path):
        return self._base_url + path

    def _build_headers(self):
        headers = {
            'Content-Type': 'application/json'
        }

        if self._access_token:
            headers['apikey'] = self._access_token

        return headers

    def _parse_response(self, response):
        if 200 <= response.status_code < 300:
            return self._value_for_response(response)
        else:
            raise self._exception_for_response(response)

    def _value_for_response(self, response):
        if response.text.strip():
            return GenericModel.from_json(response.text)
        else:
            return True

    def _exception_for_response(self, response):
        if response.status_code == 404:
            return NotFoundError(response.reason)
        elif response.status_code == 400 and 'OAuthException' in response.text:
            return InvalidAccessTokenError(response.reason)
        elif response.status_code == 401:
            return UnauthorizedError(response.reason)
        elif response.status_code == 403:
            return ForbiddenError(response.reason)
        elif response.status_code == 429:
            return RateLimitExceededError(response.reason)
        else:
            return ResponseError(
                u'{} error: {}\nresponse: {}'.format(
                    response.status_code,
                    response.reason,
                    response.text,
                )
            )
