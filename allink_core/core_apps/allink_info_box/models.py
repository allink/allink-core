# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin

from allink_core.core.utils import get_additional_templates


class AllinkInfoBoxPlugin(CMSPlugin):
    DISPLAY_DURATION = (
        (0, _('Always visible')),
        (1, _('1x')),
        (2, _('2x')),
        (3, _('3x')),
        (4, _('4x')),
        (5, _('5x')),
    )

    counter = models.IntegerField(
        _('Display duration'),
        help_text=_('After how many times/clicks should the box not be visible anymore'),
        choices=DISPLAY_DURATION,
        default=0
    )
    transparent_background = models.BooleanField(
        _('Transparent background'),
        default=False
    )
    template = models.CharField(
        _('Template'),
        help_text=_('Choose a template.'),
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
