import logging
import requests

from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook


class FivetranHook(BaseHook):
    """
    HTTP Hook that does not required a 'pre-configured' connection.
    """

    def __init__(self,
                 fivetran_token,
                 method='GET',
                 url='https://api.fivetran.com/v1/connectors/',
                 fivetran_conn_id,
                 connector_id):

        conn_id = self.get_connection(fivetran_conn_id) 
        if conn_id.extra_dejson.get('token'):
            self.fivetran_token = conn_id.extra_dejson.get('token')        

        self.method = method
        
        if conn.host:
            self.url = conn.host
        else:
            self.url = url
        
        self.connector_id = connector_id

    def get_conn(self, headers):
        """
        Returns http session for use with requests
        """
        session = requests.Session()

        if headers:
            session.headers.update(headers)

        return session
        

    def run(self, endpoint=None, data=None, headers=None, extra_options=None):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Basic %s' % self.api_token}
        extra_options = extra_options or {}
        session = self.get_conn(headers)

        url = self.url + self.connector_id # + extra options?
        req = None
        if self.method == 'GET':
            # GET uses params
            req = requests.Request(self.method,
                                   url,
                                   params=data,
                                   headers=headers)
        #else patch or post
        prepped_request = session.prepare_request(req)
        logging.info("Sending '" + self.method + "' to url: " + url)
        return self.run_and_check(session, prepped_request, extra_options)

    def run_and_check(self, session, prepped_request, extra_options):
        """
        Grabs extra options like timeout and actually runs the request,
        checking for the result
        """
        extra_options = extra_options or {}

        response = session.send(
            prepped_request,
            stream=extra_options.get("stream", False),
            verify=extra_options.get("verify", False),
            proxies=extra_options.get("proxies", {}),
            cert=extra_options.get("cert"),
            timeout=extra_options.get("timeout"),
            allow_redirects=extra_options.get("allow_redirects", True)
        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            # Tried rewrapping, but not supported. This way, it's possible
            # to get reason and code for failure by checking first 3 chars
            # for the code, or do a split on ':'
            logging.error("HTTP error: " + response.reason)
            if self.method != 'GET':
                # The sensor uses GET, so this prevents filling up the log
                # with the body every time the GET 'misses'.
                # That's ok to do, because GETs should be repeatable and
                # all data should be visible in the log (no post data)
                logging.error(response.text)
            raise AirflowException(str(response.status_code) + ":" + response.reason)
        return response
