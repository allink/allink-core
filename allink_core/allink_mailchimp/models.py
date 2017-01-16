# -*- coding: utf-8 -*-
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
from cms.models.pluginmodel import CMSPlugin


@python_2_unicode_compatible
class AllinkSignupFormPlugin(CMSPlugin):

    def __str__(self):
        return u''
