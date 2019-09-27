# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from cms.models.pluginmodel import CMSPlugin


@python_2_unicode_compatible
class AllinkSEOAccordionContainerPlugin(CMSPlugin):
    """
    A Container-Plugin for SEO Accordion content
    """

    def __str__(self):
        return _('{}').format(str(self.pk))


@python_2_unicode_compatible
class AllinkSEOAccordion(CMSPlugin):
    title = models.CharField(
        _('Title'),
        max_length=255
    )

    def __str__(self):
        return '{}'.format(self.title)
