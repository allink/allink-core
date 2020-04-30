# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.template import Library

register = Library()


@register.inclusion_tag("templatetags/allink_google_tag_manager.html")
def google_tag_manager(tag_id=''):
    if not tag_id and hasattr(settings, 'GOOGLE_TAG_MANAGER_ID'):
        tag_id = settings.GOOGLE_TAG_MANAGER_ID
    return {
        'tag_id': tag_id
    }
