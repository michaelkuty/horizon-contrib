
from __future__ import absolute_import

import json
import logging

import requests
from django.conf import settings
from horizon import messages
from horizon_contrib.utils import to_dotdict

LOG = logging.getLogger("client.base")

TOKEN_FORMAT = "  Token {0}"


class ClientBase(object):

    """Base Client Object with main method ``request``
    """

    def __init__(self, **kwargs):
        super(ClientBase, self).__init__(**kwargs)

        try:
            self.set_api()
        except Exception, e:
            LOG.exception(e)

    def request(self, path, method="GET", params={}, request={}):
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
        headers = {}

        _request = request
        self.set_api()
        LOG.debug("%s - %s%s - %s" % (method, self.api, path, params))

        if method == "GET":
            request = requests.get('%s%s' % (self.api, path), headers=headers)
        elif method == "POST":
            headers["Content-Type"] = "application/json"
            request = requests.post(
                '%s%s' % (self.api, path), data=json.dumps(params), headers=headers)
        elif method == "PUT":
            headers["Content-Type"] = "application/json"
            request = requests.put(
                '%s%s' % (self.api, path), data=json.dumps(params), headers=headers)
        elif method == "DELETE":
            request = requests.delete(
                '%s%s' % (self.api, path), data=json.dumps(params), headers=headers)

        if request.status_code in (200, 201):
            result = request.json()
            if "error" in result:
                msg = result.get("error")
                # populate exception
                messages.error(_request, msg)
                if settings.DEBUG:
                    raise Exception(msg)
            return to_dotdict(result)
        else:
            if getattr(settings, "DEBUG", False):
                msg = "url: %s%s, method: %s, status: %s" % (
                    self.api, path, method, request.status_code)
            else:
                msg = "Unexpected exception."
            if request.status_code == 401:
                raise Unauthorized
            if request.status_code == 400:
                raise BadRequest
            if request.status_code == 500:
                raise Exception(request.body)
            messages.error(_request, msg)
            raise ClientException("Unhandled response status %s" % request.status_code)

    def set_api(self):
        self.api = '%s://%s:%s%s' % (getattr(self, "protocol", "http"), getattr(
            self, "host", "127.0.0.1"), getattr(self, "port"), getattr(self, "api_prefix", "/api"))
