# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django import template
from cms.models import Page

register = template.Library()


@register.assignment_tag(takes_context=True)
def members_index_page_full_url(context):
    """
    returns url of members index page full
    used mainly for js window.location.href
    """
    try:
        page = Page.objects.published().filter(application_namespace='members').order_by('-path')[0]
        return context.request.build_absolute_uri(page.get_absolute_url())
    except IndexError:
        raise IndexError('Apphook for members area is not defined. Please hook it to the desired page.')


@register.simple_tag()
def members_index_page_url():
    """
    returns url of members index page full
    """
    try:
        return Page.objects.published().filter(application_namespace='members').order_by('-path')[0].get_absolute_url()
    except IndexError:
        raise IndexError('Apphook for members area is not defined. Please hook it to the desired page.')
