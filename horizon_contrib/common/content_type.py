from django.contrib.contenttypes.models import ContentType

"""
helper for searching Content Type
"""


def get_class(name):
    """return model class
    """

    model_class = None
    for content_type in ContentType.objects.all():
        if content_type.model.lower() == unicode(name):
            model_class = content_type.model_class()
            break

    if model_class is None:
        raise Exception("get class by string: Neznama trida: %s " % name)

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
