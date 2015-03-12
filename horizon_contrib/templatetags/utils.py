from django import template
from horizon_contrib.forms import SelfHandlingModelForm

register = template.Library()


@register.filter
def ismodelform(form):
    return isinstance(form, SelfHandlingModelForm)
