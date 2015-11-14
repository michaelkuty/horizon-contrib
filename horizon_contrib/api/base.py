
import json
import logging

import requests
from requests import exceptions
from django.conf import settings
from horizon import messages
from .response import ListResponse, DictResponse

LOG = logging.getLogger("client.base")

TOKEN_FORMAT = "  Token {0}"


class ClientBase(object):

    """Base Client Object with main method ``request``

    this is only simple wrapper which is overwritten in 99%

    but provide consitent request method

    """

    list_response_class = ListResponse
    dict_response_class = DictResponse

    def do_request(self, path, method="GET", params={}, headers={}):
        '''make raw request'''

        if not method == 'GET' and path[-1] != '/':
            path = path + '/'

        if method == "GET":
            response = requests.get(path, headers=headers)
        elif method == "POST":
            headers["Content-Type"] = "application/json"
            response = requests.post(
                path,
                data=json.dumps(params),
                headers=headers)
        elif method == "PUT":
            headers["Content-Type"] = "application/json"
            response = requests.put(
                path,
                data=json.dumps(params),
                headers=headers)
        elif method == "DELETE":
            response = requests.delete(
                path,
                data=json.dumps(params),
                headers=headers)
        return response

    def process_response(self, response, request):
        '''process response and handle statues and exceptions'''

        if response.status_code <= 204:
            result = response.json()
            if "error" in result:
                msg = result.get("error")
                # populate exception
                messages.error(request, msg)
                if settings.DEBUG:
                    LOG.exception(msg)
            return result
        else:
            if response.status_code == 401:
                raise exceptions.HTTPError('Unautorized 401')
            if response.status_code == 400:
                raise exceptions.HTTPError('Bad Request 400')
            if response.status_code == 500:
                LOG.exception(request.body)
                raise exceptions.HTTPError('Unexpected exception 500')
            return Exception(response.status_code)

    def process_data(self, result, request):
        '''process result and returns data'''

        if isinstance(result, list):
            response = self.list_response_class(result)
        elif isinstance(result, dict):
            response = self.dict_response_class(result)

        return response

    def process_headers(self, headers, request):
        '''process headers for example add auth headers'''
        return headers

    def process_params(self, params, request):
        '''process params'''
        return params

    def process_method(self, method, request):
        '''process method'''
        return method

    def process_url(self, url, request):
        '''process url'''
        return url

    def process_exception(self, exception, request, response):
        '''process exception'''
        raise exception

    def request(self, path, method="GET", params={}, request={}, headers={}):
        """main method which provide

        .. attribute:: path

        Relative URI '/projects' -> <self.api>/projects

        .. attribute:: method

        String Rest method

        .. attribute:: params

        Dictionary data which will be serialized to json

        .. attribute:: request

        Original request where lives user
        with permissions AUTH_TOKEN or something else

        If is provided, additional messages will be pushed.

        """

        _request = request
        self.set_api()

        LOG.debug("%s - %s%s - %s" % (method, self.api, path, params))

        try:
            # do request
            response = self.do_request(
                self.process_url('%s%s' % (self.api, path), _request),
                self.process_method(method, _request),
                self.process_params(params, _request),
                self.process_headers(headers, _request))

            # process response
            result = self.process_response(response, _request)
            # process data
            data = self.process_data(result, _request)
        except Exception as e:
            self.process_exception(e, _request, response)
        else:
            return data

    def set_api(self):
        self.api = '%s://%s:%s%s' % (
            getattr(self, "protocol", "http"),
            getattr(self, "host", "127.0.0.1"),
            getattr(self, "port"),
            getattr(self, "api_prefix", "/api"))
