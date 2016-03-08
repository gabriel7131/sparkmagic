# Copyright (c) 2015  aggftw@gmail.com
# Distributed under the terms of the Modified BSD License.

from remotespark.utils.utils import get_connection_string_elements
from .linearretrypolicy import LinearRetryPolicy
from .reliablehttpclient import ReliableHttpClient


class LivyReliableHttpClient(object):
    """Default headers."""

    def __init__(self, url, username, password, retry_policy):
        self._http_client = ReliableHttpClient(url, {"Content-Type": "application/json"},
                                               username, password, retry_policy)

    @staticmethod
    def from_connection_string(connection_string):
        cso = get_connection_string_elements(connection_string)

        retry_policy = LinearRetryPolicy(seconds_to_sleep=5, max_retries=5)
        return LivyReliableHttpClient(cso.url, cso.username, cso.password, retry_policy)

    def post_statement(self, session_id, data):
        return self._http_client.post(self._statements_url(session_id), [201], data).json()

    def get_statement(self, session_id, statement_id):
        return self._http_client.get(self._statement_url(session_id, statement_id), [200]).json()

    def post_session(self, properties):
        return self._http_client.post("/sessions", [201], properties).json()

    def get_session(self, session_id):
        return self._http_client.get(self._session_url(session_id), [200]).json()

    def delete_session(self, session_id):
        self._http_client.delete(self._session_url(session_id), [200, 404])

    def get_all_session_logs(self, session_id):
        return self._http_client.get(self._session_url(session_id) + "/log?from=0", [200]).json()

    @staticmethod
    def _session_url(session_id):
        return "/sessions/{}".format(session_id)

    @staticmethod
    def _statements_url(session_id):
        return "/sessions/{}/statements".format(session_id)

    @staticmethod
    def _statement_url(session_id, statement_id):
        return "/sessions/{}/statements/{}".format(session_id, statement_id)
