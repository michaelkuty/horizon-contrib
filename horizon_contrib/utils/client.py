
import requests 
import json
import logging
from horizon import messages
from django.conf import settings

log = logging.getLogger('utils.make_request')


class Req(object):
    """
    """
    
    def __init__(self, *args, **kwargs):
        super(Req, self).__init__(*args, **kwargs)

    @staticmethod
    def make_request(path, method="GET", params={}, request=None):
        """small util method for simplify create request with handled exceptions
        and debug output

        .. attribute:: path

            Required.

        .. attribute:: method

            The HTTP method for this action. Defaults to ``GET``. Other methods
            may or may not succeed currently.

        .. attribute:: params

            Default to be an empty dictionary (``{}``)

        .. attribute:: request

            Django request object. Provides django messages.
            Useful in debug. 

        """
        log.debug("%s - %s - %s"%(method,path,params))

        if method == "GET":
            response = requests.get(path)

        elif method in ["POST", "PUT", "DELETE"]:
            headers = {"Content-Type": "application/json" }
            req = requests.Request(method, path, data=json.dumps(params),headers=headers).prepare()
            response = requests.Session().send(req)

        try:
            response = response.json()
        except Exception, e:

            """delete ok"""
            if response.status_code == 204:
                return True

            if request:
                """handle errors"""
                messages.error(request, "%s - %s - %s - %s - %s" % (method, path, params, response.status_code, str(response.text)))
                return {}
            return { 'status_code': response.status_code, 'text': response.text }
        return response

class BaseClient(object):
    """small util class for easy api manipulate

    .. attribute:: host

        Required.

    .. attribute:: port

        Required.

    .. attribute:: api_prefix

        Default to be a string (``api``)

    .. attribute:: protocol

        Optional.

    """

    host = None
    port = None
    protocol = "http"
    api_prefix = "/api"

    req = Req()

    @property
    def api(self):
        return  '{0}://{1}:{2}{3}'.format(self.protocol.lower(),
                                            self.host, 
                                            self.port,
                                            self.api_prefix)

    def request(self, *args, **kwargs):
        """small util method for simplify create request with handled exceptions
        and debug output

        .. attribute:: path

            Required.

        .. attribute:: method

            The HTTP method for this action. Defaults to ``GET``. Other methods
            may or may not succeed currently.

        .. attribute:: params

            Default to be an empty dictionary (``{}``)

        .. attribute:: request

            Django request object. Provides django messages.
            Useful in debug. 

        """
        url = args[0]
        method = "GET"
        data = {}
        request = None
        try:
            method = args[1]
            data = args[2]
        except Exception, e:
            pass

        try:
            request = args[3]
        except Exception, e:
            pass

        if not url:
            url = kwargs.get("url", "")
        _url = "{0}{1}".format(self.api, url)
        return self.req.make_request(path=_url,method=method, params=data, request=request)

    def __init__(self, *args, **kwargs):
        super(BaseClient, self).__init__(*args, **kwargs)
