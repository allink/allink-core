# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings

_base_url = None


def base_url():
    from django.contrib.sites.models import Site
    global _base_url
    if not '_base_url' not in locals() or not _base_url:
        _base_url = 'http://' + Site.objects.get_current().domain
    return _base_url


def get_additional_templates(model_name):
    """
    Get additional templates choices from settings for model_name
    """
    config = '{}_PLUGIN_TEMPLATES'.format(model_name.upper())
    additional_templates = getattr(settings, config, ())
    return additional_templates


def get_additional_choices(config):
    """
    Get additional settings var for project specific configuration
    """
    try:
        return getattr(settings, config, ())
    # TODO: specify Error type
    except:
        return ''


def get_project_color_choices():
    """
    returns all projects specific colors
    """
    from allink_core.allink_base.models.choices import BLANK_CHOICE
    return BLANK_CHOICE + settings.PROJECT_COLORS


def get_ratio_choices():
    """
    returns all projects specific ratio choices
    """
    from allink_core.allink_base.models.choices import BLANK_CHOICE, RATIO_CHOICES
    return BLANK_CHOICE + RATIO_CHOICES + get_additional_choices('RATIO_CHOICES')


def get_height_from_ratio(width, ratio_w, ratio_h):
    """
    Used to calculate thumbnail height from given width and ratio
    """
    return width * ratio_h / ratio_w


