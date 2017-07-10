# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from cms.models.pluginmodel import CMSPlugin

@python_2_unicode_compatible
class AllinkPdfPageBreakPlugin(CMSPlugin):
    """
    A Plugin for telling the pdf export to do a page break
    """

    pass
