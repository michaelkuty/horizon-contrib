# -*- coding: UTF-8 -*-

from horizon_contrib.api.base import ClientBase


class Manager(ClientBase):

    """base manager class which provide consistent interface
    for working with API
    in many cases you want add extra method
    like an object specific actions subscribe/like etc
    its only interface not golden rule
    """

    def all(self, *args, **kwargs):
        return []

    def get(self, *args, **kwargs):
        return NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    # common stuff
    def order_by(self, *args, **kwargs):
        raise NotImplementedError

    def filter(self, *args, **kwargs):
        raise NotImplementedError
