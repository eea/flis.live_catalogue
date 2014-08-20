import re
import os

from django import template
from django.conf import settings
from live_catalogue.auth import is_admin


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


@register.filter
def filename(value):
    return os.path.basename(value.file.name)


@register.assignment_tag(name='is_admin', takes_context=True)
def do_is_admin(context):
    return True if is_admin(context['request']) else False