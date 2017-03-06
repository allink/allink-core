# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")


@register.assignment_tag
def var(val=None):
  return val
