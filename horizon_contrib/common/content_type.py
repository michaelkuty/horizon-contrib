
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from .model_registry import get_model

"""
helper for searching Content Type
"""


def get_class_from_ct(name):
    """return model class
    """

    if not name:
        return name

    model_class = None
    for content_type in ContentType.objects.all():
        if content_type.model.lower() == name.lower():
            model_class = content_type.model_class()
            break

    if model_class is None:
        raise Exception(
            _("get class by string: Unknown class: %s " % name.lower()))

    return model_class


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
    """this method try to find model fron CT or our registry
    all generic features depends on this method

    for this time only recall get_class_from_ct because our registiry
    does not exists
    """

    # if CT enabled search in
    if _is_contenttypes_enabled():
        return get_class_from_ct(name)
    # in our registry
    return get_model(name)
