# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from cms.models.pluginmodel import CMSPlugin


@python_2_unicode_compatible
class AllinkSignupFormPlugin(CMSPlugin):

    SIGNUP_FORMS = (
        ('simple', 'Simple'),
        ('advanced', 'Advanced')
    )

    signup_form = models.CharField(
        _(u'Template'),
        help_text=_(u'Choose a form.'),
        max_length=50,
        choices=SIGNUP_FORMS,
        default=SIGNUP_FORMS[0]
    )

    def __str__(self):
        return u''
