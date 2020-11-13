# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from allink_core.core.models.base_plugins import AllinkBaseFormPlugin
from allink_core.core.models.choices import SALUTATION_CHOICES


class DummyAppSignup(TimeStampedModel):
    salutation = models.IntegerField(
        _('Salutation'),
        choices=SALUTATION_CHOICES,
    )

    first_name = models.CharField(
        _('First Name'),
        max_length=255,
    )

    last_name = models.CharField(
        _('Last Name'),
        max_length=255,
    )

    place = models.CharField(
        _('Place'),
        max_length=255,
        blank=True,
    )

    email = models.EmailField(
        _('Email'),
        null=True
    )


class DummyAppSignupPlugin(AllinkBaseFormPlugin):
    pass
