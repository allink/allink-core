# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from cms.models.pluginmodel import CMSPlugin

from allink_core.allink_base.utils import get_additional_templates

@python_2_unicode_compatible
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
        _(u'Display duration'),
        help_text=_(u'After how many times/clicks should the box not be visible anymore'),
        choices=DISPLAY_DURATION,
        default=0
    )
    transparent_background = models.BooleanField(
        _(u'Transparent background'),
        default=False
    )
    template = models.CharField(
        _(u'Template'),
        help_text=_(u'Choose a template.'),
        max_length=50
    )

    def get_templates(self):
        templates = ()
        for x, y in get_additional_templates('Infobox'):
            templates += ((x, y),)
        return templates

    def __str__(self):
        if self.template:
            return u'({})'.format(self.template)
        return str(self.pk)
