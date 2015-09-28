# -*- coding: utf-8 -*-
import django

from distutils.version import StrictVersion

from django.db import models

"""
these method is used in ``SelfHandlingModalForm`` for easily save model
because django < 1.7 not supported update_or_create
https://docs.djangoproject.com/en/1.7/ref/models/querysets/#django.db.models.query.QuerySet.update_or_create
"""


def create_or_update_and_get(model_class, data):

    if StrictVersion(django.get_version()) > StrictVersion('1.7'):
        # (majklk) TODO use native django update_or_create
        if model_class._meta.pk.name in data:
            model_pk_name = model_class._meta.pk.name
            obj, created = model_class.objects.update_or_create(
                **{model_pk_name: data.pop(model_pk_name), 'defaults': data})
            return obj
    else:
        # note we assume data is already deserialized to a dict
        if model_class._meta.pk.name in data:
            get_or_create_kwargs = {
                model_class._meta.pk.name: data.pop(model_class._meta.pk.name)
            }
            try:
                # get
                instance = model_class.objects.get(**get_or_create_kwargs)
            except model_class.DoesNotExist:
                # create
                instance = model_class(**get_or_create_kwargs)
        else:
            # create
            instance = model_class()

        # update (or finish creating)
        for key, value in list(data.items()):
            field = model_class._meta.get_field(key)
            if not field:
                continue
            if isinstance(field, models.ManyToManyField):
                # can't add m2m until parent is saved
                continue
            elif isinstance(field, models.ForeignKey) and hasattr(value, 'items'):
                rel_instance = create_or_update_and_get(field.rel.to, value)
                setattr(instance, key, rel_instance)
            else:
                setattr(instance, key, value)
        instance.save()
        # now add the m2m relations
        for field in model_class._meta.many_to_many:
            if field.name in data and hasattr(data[field.name], 'append'):
                for obj in data[field.name]:
                    rel_instance = create_or_update_and_get(field.rel.to, obj)
                    getattr(instance, field.name).add(rel_instance)
        return instance
