from .utils import HttpTestCase
from mock import patch

from respy import Client
from respy.errors import *


class ClientGetTest(HttpTestCase):

    def test_get_parses_json(self):
        self.stub_get_requests(
            response_body='{"messages": ["first", "second"]}',
        )
        client = Client(access_token="abc123")

        messages = client.get('/social')

        self.assertEqual(messages.messages, ["first", "second"])    

    def test_get_uses_default_base_url(self):
        self.stub_get_requests()
        client = Client(access_token="abc123")

        client.get('/social')

        self.assert_get_request("http://res.storystream.it:3000/social")

    def test_get_uses_custom_base_url(self):
        self.stub_get_requests()
        client = Client(access_token="1a2bc3", base_url="https://example.com")

        client.get('/social')

        self.assert_get_request("https://example.com/social")

    def test_get_sends_authorization_header(self):
        self.stub_get_requests()
        client = Client(access_token="abc123")

        client.get("/users/123")

        self.assert_get_request(
            url="http://res.storystream.it:3000/users/123",
            headers={'Content-Type': 'application/json', "Authorization": "Bearer abc123"},
        )

    def test_get_does_not_send_authorization_header_with_no_token(self):
        self.stub_get_requests()
        client = Client(access_token=None)

        client.get('/social')

        self.assert_get_request(
            url="http://res.storystream.it:3000/social",
            headers={'Content-Type': 'application/json'},
        )

    def test_get_sends_query_string_parameters(self):
        self.stub_get_requests()
        client = Client(access_token="456efg")

        client.get("/social", include_shares=True)

        self.assert_get_request(
            url="http://res.storystream.it:3000/social",
            params={"include-shares": 'true'},
        )

    def test_get_handles_invalid_access_token_responses(self):
        self.stub_get_requests(
            response_status=400,
            response_body="""{
                "error": {
                    "type": "OAuthException",
                    "message": "Error validating access token."
                 }
             }""",
        )
        client = Client(access_token="456efg")

        self.assertRaises(InvalidAccessTokenError, client.get, '/social')

    def test_get_handles_unauthorized_responses(self):
        self.stub_get_requests(response_status=401)
        client = Client(access_token="456efg")

        self.assertRaises(UnauthorizedError, client.get, '/social')

    def test_get_handles_rate_limit_error_responses(self):
        self.stub_get_requests(response_status=429)
        client = Client(access_token="abc")

        self.assertRaises(RateLimitExceededError, client.get, "/user/1")

    def test_get_handles_not_found_responses(self):
        self.stub_get_requests(response_status=404)
        client = Client(access_token="456efg")

        self.assertRaises(NotFoundError, client.get, "/not/real")

    def test_get_handles_unexpected_http_responses(self):
        self.stub_get_requests(response_status=500)
        client = Client(access_token="abcdef")

        self.assertRaises(ResponseError, client.get, '/social')
