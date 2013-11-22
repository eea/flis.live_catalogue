import re
from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, pattern):
    request = context['request']
    pattern = '^%s/' + pattern
    if getattr(settings, 'FORCE_SCRIPT_NAME', None):
        pattern = pattern % settings.FORCE_SCRIPT_NAME
    else:
        pattern = pattern % ''

    if re.search(pattern, request.path):
        return 'active'
    return ''


@register.assignment_tag
def assign(value):
    return value
