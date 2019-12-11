from django import template

register = template.Library()

@register.filter(name='div')
def div(value, arg):
    return int(value/arg)