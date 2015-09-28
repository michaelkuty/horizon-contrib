
from django.core.urlresolvers import reverse
from django.contrib.admin.templatetags.admin_list import result_list
from django import template

from django.template.loader import render_to_string
from django.utils.html import format_html
register = template.Library()

def is_empty(array):
    if len(array) == 0:
        return True
    else:
        return False

@register.filter
def issue_list(array):
    """
    """
    url = "horizon:common:ukol:detail"
    ul = "<ul class=\"list-group\">{0}</ul>"
    li = "<li class=\"list-group-item\">{0}</li>"
    _link = "<a class=\"ajax-modal\" href=\"{0}\">{1}</a>"
    lis = []
    if is_empty(array):
        return "-"
    for model_issue in array:
        link = _link.format(reverse(url, args=(model_issue.issue.id,)), model_issue) 
        lis.append(li.format(link))
    ul = ul.format("".join(lis))
    return format_html(ul)

@register.filter
def list(array):
    """
    """
    ul = "<ul class=\"list-group\">{0}</ul>"
    li = "<li class=\"list-group-item\">{0}</li>"
    lis = []
    if is_empty(array):
        return "-"
    for value in array:
        lis.append(li.format(value))
    ul = ul.format("".join(lis))
    return format_html(ul)

@register.filter
def line_list(array):
    if is_empty(array):
        return "-"
    try:
        _array = []
        for item in array:
            _array.append(item.__unicode__())
        array = _array
    except Exception as e:
        pass
    return ", ".join(array)

@register.filter
def form_group(instance, group_fields):
    """
    attribute:: instnace
    attribute:: fields :: ["string"]
    """
    label = "<label class=\"control-label\" for=\"{0}\">{0}</label>"
    input = "<input class=\"form-control\" id=\"{0}\" type=\"text\" value=\"{1}\">"
    inputs = []
    
    if instance is None: return ""
   
    for field in group_fields:
        field_name = instance._meta.get_field_by_name(field)[0].name #name je vzdycky
        field_name = instance._meta.get_field_by_name(field)[0].verbose_name
        field_label = field_name.capitalize()
        value = getattr(instance, field, "-")
        if not value or len(str(value)) == 0:
            value = "-"
        inputs.append("{0}{1}".format(label.format(field_label), input.format(field_label, value)))
    
    return format_html("".join(inputs))

@register.filter
def div_group(instance, group_fields):
    """
    attribute:: instnace
    attribute:: fields :: ["string"]
    """
    label = "<div class=\"list-label\" for=\"{0}\">{0}:</div>"
    input = "<div class=\"list-value\" id=\"{0}\">&nbsp;{1}</div>"
    inputs = []
    
    if instance is None: return ""
   
    for field in group_fields:
        field_name = instance._meta.get_field_by_name(field)[0].name #name je vzdycky
        field_name = instance._meta.get_field_by_name(field)[0].verbose_name
        field_label = field_name.capitalize()
        value = getattr(instance, field, "-")
        if not value or len(str(value)) == 0:
            value = "-"
        inputs.append("{0}{1}".format(label.format(field_label), input.format(field_label, value)))
    
    return format_html("".join(inputs))