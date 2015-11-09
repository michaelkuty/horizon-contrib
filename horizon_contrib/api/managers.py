# -*- coding: UTF-8 -*-

import operator
from horizon_contrib.api.base import ClientBase
from urllib import urlencode


class SearchOptionsMixin(object):

    '''Encapsulation of search options'''

    def get_search_options(self, opts={}):
        '''merge search options with defaults'''
        opts.update(getattr(self, 'search_options', {}))
        return opts

    def get_query_string(self, search_opts):
        '''returns query string from search options'''
        return urlencode(self.get_search_options(search_opts))

    def get_url(self, id=None, search_opts={}):
        query = self.get_query_string(search_opts)
        if not id:
            base_url = '/%s/' % self.scope
        else:
            base_url = '/{0}/{1}/'.format(self.scope, id)
        if query:
            return '?'.join([base_url,
                            query])
        return base_url


class Manager(ClientBase, SearchOptionsMixin):

    """base manager class which provide consistent interface
    for working with API
    in many cases you want add extra method
    like an object specific actions subscribe/like etc
    its only interface not golden rule

    :attr:scope: string which specify api uri::

        scope = 'tickets'

    will produce -> api/tickets
    """

    def all(self, *args, **kwargs):
        return self.list(*args, **kwargs)

    def get(self, id, request=None):
        return self.request(
            self.get_url(id),
            'GET',
            request=request)

    def create(self, data, request=None):
        return self.request(
            self.get_url(),
            'POST',
            params=data,
            request=request)

    def update(self, id, data, request=None):
        return self.request(
            self.get_url(id),
            'PUT',
            params=data,
            request=request)

    def delete(self, id, request=None, *args, **kwargs):
        return self.request(
            self.get_url(id),
            'DELETE',
            request=request)

    def list(self, request=None, search_opts={}):
        return self.request(
            self.get_url(search_opts=search_opts),
            'GET',
            request=request)

    def choices(self, request, data=None, pk='id',
                label='{hostname}', name='Host', empty=True):
        '''make choices from data or self.list

        data for making choices
        label is string with item context
        name is singular name of item
        if you want create multiple choices use empty=False
        '''
        choices = []
        if not data:
            data = self.list(request)
        for item in data:
            choices.append((item[pk], label.format(**item)))
        if choices:
            choices.sort(key=operator.itemgetter(1))
            if empty:
                choices.insert(0, ("", "Select %s" % name))
        else:
            choices.insert(0, ("", "No %s available" % name))
        return choices

    # other common stuff

    def order_by(self, *args, **kwargs):
        raise NotImplementedError

    def filter(self, *args, **kwargs):
        raise NotImplementedError
