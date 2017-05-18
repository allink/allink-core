# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings


_base_url = None


def base_url():
    from django.contrib.sites.models import Site
    global _base_url
    if not '_base_url' not in locals() or not _base_url:
        _base_url = 'https://' + Site.objects.get_current().domain
    return _base_url


def get_additional_templates(model_name):
    """
    Get additional templates choices from settings for model_name
    """
    config = '{}_PLUGIN_TEMPLATES'.format(model_name.upper())
    additional_templates = getattr(settings, config, ())
    return additional_templates


def get_additional_choices(config, blank=False):
    """
    Get additional settings var for project specific configuration
    """
    from allink_core.allink_base.models.choices import BLANK_CHOICE
    choices = ()
    if blank:
        choices = BLANK_CHOICE
    choices += getattr(settings, config, ())
    return choices


def get_project_color_choices():
    """
    returns all projects specific colors
    """
    return getattr(settings, 'PROJECT_COLORS', {})


def get_ratio_choices():
    """
    returns all projects specific ratio choices
    """
    from allink_core.allink_base.models.choices import BLANK_CHOICE, RATIO_CHOICES
    return BLANK_CHOICE + RATIO_CHOICES + get_additional_choices('RATIO_CHOICES')


def get_ratio_choices_orig():
    """
    returns all projects specific ratio choices
    """
    from allink_core.allink_base.models.choices import BLANK_CHOICE, RATIO_CHOICES_ORIG
    return BLANK_CHOICE + RATIO_CHOICES_ORIG + get_additional_choices('RATIO_CHOICES')


def get_height_from_ratio(width, ratio_w, ratio_h):
    """
    Used to calculate thumbnail height from given width and ratio
    """
    return width * ratio_h / ratio_w


def get_percent(full, value):
    """
    returns a value in percent. (how much percent of ..)
    rounded whole numbers
    """
    return round(value * (100 / full))


def get_ratio_w_h(ratio):
    """
    returns width and height from string e.g. '1-2' or '4-3' as integer
    """
    w, h = ratio.split('-')
    return int(w), int(h)


def get_display(key, list):
    """
    returns key from list of tuples
    """
    d = dict(list)
    try:
        return d.get(int(key))
    except:
        return None


def replace_line_breaks(string):
    """
    replaces
    '\r\n' and '\n\r' and '\r' and '\n' and with '<br />'
    """
    r = '<br />'
    return string.replace('\r\n', r).replace('\n\r', r).replace('\r', r).replace('\n', r)
