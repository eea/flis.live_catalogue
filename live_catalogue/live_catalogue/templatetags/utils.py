from datetime import datetime
import re
import os
import calendar

from django import template
from django.conf import settings
from live_catalogue.auth import is_admin
from live_catalogue.models import Catalogue


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


@register.assignment_tag(takes_context=True)
def new_items(context, closed):
    request = context['request']
    if closed:
        last_viewed = request.session.get('closed_last_viewed')
        catalogues = Catalogue.objects.filter(
            status__in=(Catalogue.CLOSED, Catalogue.SOLVED))
    else:
        last_viewed = request.session.get('open_last_viewed')
        catalogues = Catalogue.objects.filter(status=Catalogue.OPEN)

    if not last_viewed:
        return 0

    return catalogues.filter(
        last_updated__gt=datetime.fromtimestamp(last_viewed)
    ).count()


@register.filter
def datetime_to_timestamp(value):
    if isinstance(value, datetime):
        return calendar.timegm(value.utctimetuple())
    return
