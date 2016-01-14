from mock import Mock, ANY
import json as JSON
import requests
from unittest import TestCase


class HttpTestCase(TestCase):
    """
    Mixin providing methods for stubbing HTTP requests and asserting that
    the correct tests were made.
    """

    def setUp(self):
        self.__original_request_method = requests.request

    def tearDown(self):
        requests.request = self.__original_request_method

    def stub_get_requests(self, response_body="{}", response_status=200):
        mock_response = Mock(
            text=response_body,
            status_code=response_status,
            reason="",
        )
        requests.request = Mock(return_value=mock_response)

    def assert_get_request(self, url, json=ANY, headers=ANY):
        self.assert_request("get", url, json, headers)

    def stub_post_requests(self, response_body="{}", response_status=200):
        mock_response = Mock(
            text=response_body,
            status_code=response_status,
            reason="",
        )
        requests.request = Mock(return_value=mock_response)

    def assert_post_request(self, url, json=ANY, headers=ANY):
        self.assert_request("post", url, json, headers)

    def stub_delete_requests(self, response_body="{}", response_status=200):
        mock_response = Mock(
            text=response_body,
            status_code=response_status,
            reason="",
        )
        requests.request = Mock(return_value=mock_response)

    def assert_delete_request(self, url, json=ANY, headers=ANY):
        self.assert_request("delete", url, json, headers)

    def stub_put_requests(self, response_body="{}", response_status=200):
        mock_response = Mock(
            text=response_body,
            status_code=response_status,
            reason="",
        )
        requests.request = Mock(return_value=mock_response)

    def assert_put_request(self, url, json=ANY, headers=ANY):
        self.assert_request("put", url, json, headers)

    def assert_request(self, method, url, json=ANY, headers=ANY):
        requests.request.assert_called_with(
            method=method,
            url=url,
            headers=headers,
            json=json
        )
