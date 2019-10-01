# -*- coding: utf-8 -*-

from django.db import models
from cms.models.pluginmodel import CMSPlugin


class AllinkSignupFormPlugin(CMSPlugin):

    SIGNUP_FORMS = (
        ('simple', 'Simple'),
        ('advanced', 'Advanced')
    )

    signup_form = models.CharField(
        'Template',
        help_text='Choose a form.',
        max_length=50,
        choices=SIGNUP_FORMS,
        default=SIGNUP_FORMS[0]
    )

    def __str__(self):
        return ''
