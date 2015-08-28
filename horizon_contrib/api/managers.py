# -*- coding: UTF-8 -*-

import operator
from horizon_contrib.api.base import ClientBase


class Manager(ClientBase):

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
            '/{0}/{1}'.format(self.scope, id),
            'GET',
            request)

    def create(self, data, request=None):
        return self.request(
            '/{0}/'.format(self.scope),
            'POST',
            data,
            request)

    def update(self, id, data, request=None):
        return self.request(
            '/{0}/{1}/'.format(self.scope, id),
            'PUT',
            data,
            request)

    def delete(self, id, request=None, *args, **kwargs):
        return self.request(
            '/{0}/{1}/'.format(self.scope, id),
            'DELETE',
            request)

    def list(self, request=None):
        return self.request(
            '/%s' % self.scope,
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
