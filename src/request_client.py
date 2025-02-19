import requests

from src.request_builder import RequestBuilder


class RequestClient:

    def __init__(self, url: str,
                 username: str = None,
                 password: str = None) -> None:

        self.builder = RequestBuilder(url)
        self.username = username
        self.password = password

    def _parse_response(self, response):
        if response.status_code == 204:
            return {}, 204

        try:
            response.raise_for_status()
            return response.json(), response.status_code

        except requests.HTTPError:
            message = f'{response.reason}: {response.text}'
            return requests.HTTPError(message, response=response), response.status_code

        except ValueError:
            return response.text

    def _request(self,
                 method: str,
                 endpoint: str = None,
                 query_string: dict = None,
                 access_token: str = None,
                 **kwargs):

        build_request = self.builder.build_request(method,
                                                   endpoint,
                                                   query_string,
                                                   access_token,
                                                   self.username,
                                                   self.password,
                                                   **kwargs)

        try:
            response = requests.request(**build_request)
            return self._parse_response(response)
        except requests.RequestException as e:
            print(f"Error in request: {e}")

            return 500

    def get(self,
            endpoint: str = None,
            query_string: dict = None,
            access_token: str = None,
            **kwargs):

        return self._request('GET', endpoint, query_string, access_token, **kwargs)

    def post(self,
             endpoint: str = None,
             query_string: dict = None,
             access_token: str = None,
             **kwargs):

        return self._request('POST', endpoint, query_string, access_token, **kwargs)

    def put(self,
            endpoint: str = None,
            query_string: dict = None,
            access_token: str = None,
            **kwargs):

        return self._request('PUT', endpoint, query_string, access_token, **kwargs)

    def delete(self,
               endpoint: str = None,
               query_string: dict = None,
               access_token: str = None,
               **kwargs):

        return self._request('DELETE', endpoint, query_string, access_token, **kwargs)
