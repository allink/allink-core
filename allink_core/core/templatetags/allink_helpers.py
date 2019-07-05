# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")


@register.simple_tag
def var(val=None):
    return val


@register.filter
def add_params(value, arg):
    """ Used in connection with Django's add_preserved_filters

        Usage:
        - url|add_params:'foo=bar&yolo=no'
        - url|add_params:'foo=bar'|add_params:'motto=yolo'

        use only for admin view
    """
    first = '?'
    if '?' in value:
        first = '&'

    return value + first + str(arg)


@register.simple_tag
def build_param(value, arg):
    """ Used in connection with Django's add_preserved_filters

        Usage:
        - {% build_param 'lang' 'de' as lang_param %}
        - {% build_param 'template' 17 as templ_param %}
        - {% build_param 'template' <var_name> as templ_param %}

        use only for admin view
    """
    return value + '=' + str(arg)
