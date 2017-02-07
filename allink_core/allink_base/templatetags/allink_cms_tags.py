# -*- coding: utf-8 -*-
from django import template
from cms.models import Page

register = template.Library()


@register.simple_tag
def page_from_slug(slug):
    return Page.objects.get(slug=slug)
