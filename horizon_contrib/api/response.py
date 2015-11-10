

import logging

from horizon_contrib.utils.dotdict import dotdict

LOG = logging.getLogger("client.base")


class ListResponse(list):

    pass


class DictResponse(dotdict):

    pass
