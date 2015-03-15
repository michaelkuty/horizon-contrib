from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

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


def get_class(name):
    """this method try to find model fron CT or our registry
    all generic features depends on this method

    for this time only recall get_class_from_ct because our registiry
    does not exists
    """
    return get_class_from_ct(name)
