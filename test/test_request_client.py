import json
import httpretty

from test import BaseTestClass
from unittest.mock import MagicMock, patch

from requests.exceptions import HTTPError
from src.request_client import RequestClient


class TestRequestClient(BaseTestClass):

    @patch('src.request_client.requests')
    def test_request_get_without_auth_success(self,
                                              requests):
        mock_response = MagicMock()

        expected_response = {
            'message': 'Success'
            }

        mock_response.status_code = 200
        mock_response.json.return_value = expected_response

        requests.request.return_value = mock_response

        object_helper = RequestClient(self.api)

        result, status_code = object_helper.get()

        self.assertIsInstance(result, dict)
        self.assertEqual(status_code, 200)
        self.assertEqual(result, expected_response)

    @httpretty.activate
    def test_request_get_with_auth_error(self):

        httpretty.register_uri(httpretty.GET,
                               self.api,
                               body='{"message": "Unauthorized"}',
                               status=401)

        object_helper = RequestClient(self.api)
        result, status_code = object_helper.get()

        self.assertIsInstance(result, HTTPError)
        self.assertEqual(status_code, 401)
        self.assertEqual(str(result), 'Unauthorized: {"message": "Unauthorized"}')

    @patch('src.request_client.requests')
    def test_request_get_with_auth_basic_success(self,
                                                 requests):
        mock_response = MagicMock()

        expected_response = {
            'message': 'Success'
            }

        mock_response.status_code = 200
        mock_response.json.return_value = expected_response

        requests.request.return_value = mock_response

        object_helper = RequestClient(self.api,
                                      username='test1',
                                      password='Test12345678')

        result, status_code = object_helper.get()

        self.assertIsInstance(result, dict)
        self.assertEqual(status_code, 200)
        self.assertEqual(result, expected_response)

    @patch('src.request_client.requests')
    def test_request_get_with_auth_bearer_success(self,
                                                  requests):
        mock_response = MagicMock()

        expected_response = {
            'message': 'Success'
            }

        mock_response.status_code = 200
        mock_response.json.return_value = expected_response

        requests.request.return_value = mock_response

        object_helper = RequestClient(self.api)

        result, status_code = object_helper.get(endpoint='/api/v1/test',
                                                access_token='f1338ca26835863f671403941738a7b49e740fc0')

        self.assertIsInstance(result, dict)
        self.assertEqual(status_code, 200)
        self.assertEqual(result, expected_response)

    @patch('src.request_client.requests')
    def test_request_get_with_path(self,
                                   requests):

        mock_response = MagicMock()

        expected_response = {
            'message': 'Success'
            }

        mock_response.status_code = 200
        mock_response.json.return_value = expected_response

        requests.request.return_value = mock_response

        object_helper = RequestClient(self.api,
                                      username='test1',
                                      password='Test12345678')

        result, status_code = object_helper.get(endpoint='/api/v1/test')

        self.assertIsInstance(result, dict)
        self.assertEqual(status_code, 200)
        self.assertEqual(result, expected_response)

    @patch('src.request_client.requests')
    def test_request_get_with_query_string(self,
                                           requests):

        mock_response = MagicMock()

        expected_response = {
            'message': 'Success'
            }

        mock_response.status_code = 200
        mock_response.json.return_value = expected_response

        requests.request.return_value = mock_response

        object_helper = RequestClient(self.api,
                                      username='test1',
                                      password='Test12345678')

        result, status_code = object_helper.get(endpoint='/api/v1/test?name=test&last=test')

        self.assertIsInstance(result, dict)
        self.assertEqual(status_code, 200)
        self.assertEqual(result, expected_response)

    @patch('src.request_client.requests')
    def test_request_post_success(self,
                                  requests):
        mock_response = MagicMock()

        expected_response = {
            'message': 'added'
            }

        data = {
            'user': 'test'
            }

        mock_response.status_code = 201
        mock_response.json.return_value = expected_response

        requests.request.return_value = mock_response

        object_helper = RequestClient(self.api)
        result, status_code = object_helper.post(endpoint='/api/v1/test',
                                                 access_token='f1338ca26835863f671403941738a7b49e740fc0',
                                                 json=json.dumps(data))

        self.assertIsInstance(result, dict)
        self.assertEqual(status_code, 201)
        self.assertEqual(result, expected_response)

    @patch('src.request_client.requests')
    def test_request_post_form_urlencode_success(self,
                                                 requests):
        mock_response = MagicMock()

        expected_response = {
            'message': 'added'
            }

        data = {
            'user': 'test',
            'scope': 'offline'
            }

        mock_response.status_code = 201
        mock_response.json.return_value = expected_response

        requests.request.return_value = mock_response

        object_helper = RequestClient(self.api)
        result, status_code = object_helper.post(endpoint='/api/v1/test',
                                                 access_token='f1338ca26835863f671403941738a7b49e740fc0',
                                                 data=json.dumps(data))

        self.assertIsInstance(result, dict)
        self.assertEqual(status_code, 201)
        self.assertEqual(result, expected_response)

    @httpretty.activate
    def test_request_post_with_path_error(self):
        httpretty.register_uri(httpretty.POST,
                               self.api,
                               status=404,
                               body='{"message": "Not Found"}',
                               adding_headers={'Authorization': 'Basic dGVzdDE6VGVzdDEyMzQ1Njc4'})

        object_helper = RequestClient(self.api,
                                      username='test1',
                                      password='Test12345678')

        result, status_code = object_helper.post(endpoint='')

        self.assertIsInstance(result, HTTPError)
        self.assertEqual(status_code, 404)
        self.assertEqual(str(result), 'Not Found: {"message": "Not Found"}')

    @patch('src.request_client.requests')
    def test_request_put_success(self,
                                 requests):
        mock_response = MagicMock()

        expected_response = {
            'message': 'update'
            }

        data = {
            'user': 'test'
            }

        mock_response.status_code = 200
        mock_response.json.return_value = expected_response

        requests.request.return_value = mock_response

        object_helper = RequestClient(self.api)
        result, status_code = object_helper.put(endpoint='/api/v1/test',
                                                access_token='f1338ca26835863f671403941738a7b49e740fc0',
                                                json=json.dumps(data))

        self.assertIsInstance(result, dict)
        self.assertEqual(status_code, 200)
        self.assertEqual(result, expected_response)

    @patch('src.request_client.requests')
    def test_request_delete_success(self,
                                    requests):
        mock_response = MagicMock()

        mock_response.status_code = 204
        requests.request.return_value = mock_response

        object_helper = RequestClient(self.api)
        result, status_code = object_helper.delete(endpoint='/api/v1/test/1',
                                                   access_token='f1338ca26835863f671403941738a7b49e740fc0')

        self.assertIsInstance(result, dict)
        self.assertEqual(status_code, 204)
        self.assertEqual(result, {})
