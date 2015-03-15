
from django.db import models
from horizon_contrib.managers import Manager


class APIModel(models.Model):
    pk = models.IntegerField("ID", required=False)

    objects = Manager()

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        abstract = True
        verbose_name = "object"
        verbose_name_plural = "objects"
