
from django.db import models
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


class APIModel(models.Model, CRUDMixin):

    id = models.IntegerField("ID", null=True, blank=True)

    objects = Manager()

    def __unicode__(self):
        return str(self.pk)

    def __repr__(self):
        return str(self.pk)

    class Meta:
        abstract = True
        verbose_name = "object"
        verbose_name_plural = "objects"
