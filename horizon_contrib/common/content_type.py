
import logging
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core import exceptions
from .model_registry import get_model

LOG = logging.getLogger(__name__)

"""
helper for searching Content Type
"""


def get_class_from_ct(name):
    """return model class
    """

    if not name:
        return name

    parse = name.split('.')

    if len(parse) > 1:
        return ContentType.objects.get(
            app_label=parse[0], model__iexact=parse[1]).model_class()
    else:
        return ContentType.objects.get(model__iexact=parse[0]).model_class()

    return None


def get_content_type(model_class):
    """return content type class
    """

    content_type = None

    for _content_type in ContentType.objects.all():
        if _content_type.model.lower() == model_class.__name__.lower():
            content_type = _content_type

    if content_type is None:
        raise Exception("Undefined content type %s " % model_class)

    return content_type

# move to utils

CT_NAME = 'django.contrib.contenttypes'

WITHOUT_CT = getattr(settings, 'WITHOUT_CT', False)


def _is_contenttypes_enabled():

    if CT_NAME in getattr(settings, 'INSTALLED_APPS', [])\
            and not WITHOUT_CT:
        return True
    return False


def get_class(name):
    """this method return model class from CT or our registry
    all generic features depends on this method
    """
    cls = None
    # if CT enabled search in
    if _is_contenttypes_enabled():
        try:
            cls = get_class_from_ct(name)
        except exceptions.ImproperlyConfigured:
            LOG.warning("""
If you want fix this log message set ``WITHOUT_CT`` in you settings.py\
you have enabled CT fw but DATABASES = {} is ImproperlyConfigured
                """)
            # try to find in our registry
            cls = get_model(name)
    else:
        # in our registry
        cls = get_model(name)
    return cls
