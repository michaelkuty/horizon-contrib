
import requests 
import json
import logging
from horizon import messages
from django.conf import settings

LOG = logging.getLogger(__name__)

class Req(object):
    """
    """

    def __init__(self, *args, **kwargs):
        super(Req, self).__init__(*args, **kwargs)

    @staticmethod
    def make_request(path, method="GET", params={}, request=None, verify=True):
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

        if method == "GET":
            response = requests.get(path, verify=verify)

        elif method in ["POST", "PUT", "DELETE"]:
            headers = {"Content-Type": "application/json" }
            req = requests.Request(method, path, data=json.dumps(params),headers=headers).prepare()
            response = requests.Session().send(req, verify=verify)
            
        if request:
            messages.debug(request, "%s - %s - %s - %s - %s" % (method, path, params, response.status_code, str(response.text)))
        else:
            LOG.debug(request, "%s - %s - %s - %s - %s" % (method, path, params, response.status_code, str(response.text)))
        
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

    .. attribute:: private_token

        Optional.

    .. attribute:: private_token_name

        Optional. Default is private_token

    .. attribute:: api_prefix

        Default to be a string (``/api``)

    .. attribute:: protocol

        Optional.

    .. attribute:: verify

        Default True
        Optional. http://docs.python-requests.org/en/latest/user/advanced/

    """

    host = None
    port = None
    protocol = "HTTP"
    api_prefix = "/api"
    verify = True
    private_token = None
    private_token_name = "private_token"
    
    req = Req()

    @property
    def api(self):
        return  '{0}://{1}:{2}{3}'.format(self.protocol.lower(),
                                            self.host, 
                                            self.port,
                                            self.api_prefix)

    def request(self, path, method="GET", data={}, request=None, *args, **kwargs):
        """wrapper for request with handled exceptions
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
        request = getattr(kwargs, "request", None)

        if self.private_token:
            data[self.private_token_name] = self.private_token

        if not path:
            path = kwargs.get("path", "")
        _url = "{0}{1}".format(self.api, path)

        return self.req.make_request(path=_url,method=method, params=data, request=request, verify=self.verify)

    def __init__(self, *args, **kwargs):
        super(BaseClient, self).__init__(*args, **kwargs)
