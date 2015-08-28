
from datetime import datetime

from django.utils.safestring import SafeString


def timestamp_to_datetime(value):
    return datetime.fromtimestamp(value)


def nonbreakable_spaces(value):
    return SafeString(value.replace(' ', '&nbsp;'))


def unit_times(value):
    return SafeString('%s%s' % (value, '&times;'))


def join_list_with_comma(value):
    return ', '.join(value)


def join_list_with_newline(value):
    return SafeString('<br />'.join(value))


def join_list(value):

    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                return value
        return join_list_with_newline(value)


def status_icon(value):
    if value is True:
        return SafeString('<i class=\"icon-large fa fa-ok\"></i>')
    return SafeString('<i class=\"icon-large fa fa-remove"></i>')


def filter_m2m(datum):
    """helper for aggregation of m2m relation
    """
    items = []
    for d in datum.all():
        items.append(str(d))
    return ", ".join(items)
