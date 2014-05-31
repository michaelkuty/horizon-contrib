from django.contrib.admin.templatetags.admin_list import result_list
from django import template
from pohledavky.models import Osoba
from pohledavky.utils.tasks import get_osoba_action, get_user_issues
from django.template.loader import render_to_string
from django.utils.html import format_html
register = template.Library()

@register.filter
def list(array):
    """
    """
    ul = u"<ul class=\"list-group\">{0}</ul>"
    li = u"<li class=\"list-group-item\">{0}</li>"
    lis = []
    for value in array:
        lis.append(li.format(value))
    ul = ul.format("".join(lis))
    return format_html(ul)

@register.filter
def line_list(array):
    return ",".join(array)

@register.filter
def form_group(instance):
    """
    attribute:: instnace
    attribute:: fields :: ["string"]
    """
    label = u"<label class=\"control-label\" for=\"{0}\">{0}</label>"
    input = u"<input class=\"form-control\" id=\"{0}\" type=\"text\" value=\"{1}\">"
    inputs = []
    
    if instance is None: return ""
   
    for field in instance.sestava_fields:
        field_name = instance._meta.get_field_by_name(field)[0].name #name je vzdycky
        field_name = instance._meta.get_field_by_name(field)[0].verbose_name
        field_label = field_name.capitalize()
        value = getattr(instance, field)
        inputs.append(u"{0}{1}".format(label.format(field_label), input.format(field_label, value)))
    
    return format_html(u"".join(inputs))


@register.tag('to_list')
def to_list(_parser, token):
    try:
        parts = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
          "%r tag requires at least one argument" % token.contents.split()[0]

    return AsListNode(parts[1:])

class AsListNode(template.Node):
    def __init__(self, parts):
        self.parts = map(lambda p: template.Variable(p), parts)

    def render(self, context):
        resolved = []
        for each in self.parts:
            resolved.append(each.resolve(context))
        return resolved
