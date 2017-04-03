# -*- coding: utf-8 -*-
from django.utils.encoding import python_2_unicode_compatible
from cms.models.pluginmodel import CMSPlugin


@python_2_unicode_compatible
class AllinkSignupFormPlugin(CMSPlugin):

    def __str__(self):
        return u''
