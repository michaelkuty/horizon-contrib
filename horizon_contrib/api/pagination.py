

import logging
from math import ceil

from horizon import exceptions
from django.utils import six
from django.conf import settings
from .base import ClientBase
from .response import ListResponse

LOG = logging.getLogger("client.base")

API_RESULT_PAGE_SIZE = getattr(settings, 'API_RESULT_PAGE_SIZE', 25)


class PaginatedListResponse(ListResponse):

    '''Extend response with pagination helpers'''

    def __init__(self, data, *args, **kwargs):
        self._data = data
        super(PaginatedListResponse, self).__init__(
            data.get('results'), *args, **kwargs)

    @property
    def count(self):
        return self._data.get('count')

    @property
    def previous(self):
        return self._data.get('previous', None)

    @property
    def next(self):
        return self._data.get('next', None)

    @property
    def page_range(self):
        '''little ugly piece of pagination'''
        page_size = float(API_RESULT_PAGE_SIZE)
        count = float(self.count)
        if ceil(count / page_size) > 0:
            return six.moves.range(1, int(ceil(count / page_size)) + 1)
        return six.moves.range(1, int(ceil(count / page_size)))


class PaginationClient(ClientBase):
    '''Use pagination list reponse'''

    list_response_class = PaginatedListResponse

    def process_data(self, data, request):
        '''optionaly extract results from response'''

        # check if data are paginated
        if 'results' in data:
            response = self.list_response_class(data)
        else:
            response = data

        if 'errors' in data:
            if settings.DEBUG:
                raise Exception(data['errors'])
            exceptions.handle(request, ', '.join(data['errors']))

        return response
