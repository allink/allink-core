# -*- coding: utf-8 -*-

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from cms.models.pluginmodel import CMSPlugin


@python_2_unicode_compatible
class AllinkSEOAccordionContainerPlugin(CMSPlugin):
    """
    A Container-Plugin for SEO Accordion content
    """

    is_seo_faq = models.BooleanField(
        'Enable SEO FAQ schema',
        help_text='Enable to display accordion contents as questions/answers in search engine result pages',
        default=True
    )

    def __str__(self):
        return '{}'.format(str(self.pk))


@python_2_unicode_compatible
class AllinkSEOAccordion(CMSPlugin):
    title = models.CharField(
        'Title',
        max_length=255
    )

    def __str__(self):
        return '{}'.format(self.title)
