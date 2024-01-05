# stories/templatetags/custom_filters.py
from django import template

register = template.Library()


@register.filter(name='format_timestamp')
def format_timestamp(timestamp):
    return timestamp.strftime('%Y%m%d%H%M%S')
