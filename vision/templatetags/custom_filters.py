from django import template
import html

register = template.Library()

@register.filter
def unescape_html(value):
    if value:
        return html.unescape(value)
    return value

@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter. Usage: "a,b,c"|split:"," """
    return value.split(delimiter)
