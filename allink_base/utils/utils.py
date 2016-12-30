# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

def get_additional_templates(model_name):
    """
    Get additional templates choices from settings for model_name
    """
    config = '{}_PLUGIN_TEMPLATES'.format(model_name.upper())
    additional_templates = getattr(settings, config, ())
    return additional_templates
