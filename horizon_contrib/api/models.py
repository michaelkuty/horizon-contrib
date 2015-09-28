


import copy

import six
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from horizon_contrib.api.managers import Manager


class CRUDMixin(object):

    """
    manager provide proxies for CRUD method down to manager if is available
    """

    def save(self, *args, **kwargs):
        if hasattr(self, 'objects'):

            self.objects.save(*args, **kwargs)

    def update(self, *args, **kwargs):
        # proxy to manager if defined
        if hasattr(self, 'objects'):

            self.objects.update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # proxy to manager if defined
        if hasattr(self, 'objects'):

            self.objects.delete(*args, **kwargs)

    def create(self, *args, **kwargs):
        # proxy to manager if defined
        if hasattr(self, 'objects'):

            self.objects.create(*args, **kwargs)


@python_2_unicode_compatible
class APIModel(models.Model, CRUDMixin):

    objects = Manager()

    def __str__(self):
        return str(self.id)

    def __init__(self, *args, **kwargs):
        # here we must clean kwargs becase django raise exception
        # if field not found defined on model
        _kwargs = copy.copy(kwargs)

        field_names = [f.name for f in self._meta.fields]
        for key, value in six.iteritems(_kwargs):
            if key not in field_names:
                kwargs.pop(key)

        super(APIModel, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True
        verbose_name = "object"
        verbose_name_plural = "objects"


class DotDict(dict):

    """ Dictionary with dot access """

    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class DictModel(DotDict, models.Model):

    class Meta:
        abstract = True
        verbose_name = "object"
        verbose_name_plural = "objects"
