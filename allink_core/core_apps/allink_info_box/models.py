# -*- coding: utf-8 -*-
from django.db import models
from cms.models.pluginmodel import CMSPlugin

from allink_core.core.utils import get_additional_templates


class AllinkInfoBoxPlugin(CMSPlugin):
    DISPLAY_DURATION = (
        (0, 'Always visible'),
        (1, '1x'),
        (2, '2x'),
        (3, '3x'),
        (4, '4x'),
        (5, '5x'),
    )

    counter = models.IntegerField(
        'Display duration',
        help_text='After how many times/clicks should the box not be visible anymore',
        choices=DISPLAY_DURATION,
        default=0
    )
    transparent_background = models.BooleanField(
        'Transparent background',
        default=False
    )
    template = models.CharField(
        'Template',
        help_text='Choose a template.',
        max_length=50
    )

    def __str__(self):
        if self.template:
            return '({})'.format(self.template)
        return str(self.pk)

    def get_templates(self):
        templates = ()
        for x, y in get_additional_templates('INFOBOX'):
            templates += ((x, y),)
        return templates
