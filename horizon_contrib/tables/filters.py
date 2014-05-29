
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

def status_image(value):
    if value is True:
        return SafeString('<i class=\"halflings ok\">\E013</i>')
    return SafeString('<i class=\"btn-delete">\E013</i>')