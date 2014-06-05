from django import template

register = template.Library()

@register.filter
def currency(value): 
	if not isinstance(value, int):
		return value
	return u"%s Kč"% value