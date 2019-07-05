# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models

from allink_core.core.models import AllinkSimpleRegistrationFieldsModel, AllinkBaseFormPlugin


class BaseContactRequest(AllinkSimpleRegistrationFieldsModel):
    TIME_CHOICES = (
        (None, _('-- between --')),
        (1, u'09:00-11:00'),
        (2, u'13:00-15:00'),
        (3, u'15:00-17:00'),
    )
    CONTACT_PHONE = 10
    CONTACT_EMAIL = 20

    CONTACT_CHOICES = (
        (None, _('-- please choose --')),
        (CONTACT_PHONE, _('Phone')),
        (CONTACT_EMAIL, _('Email')),
    )

    contact_type = models.IntegerField(
        _('Please contact me via'),
        choices=CONTACT_CHOICES,
    )

    date = models.DateField(
        _('Date'),
        blank=True,
        null=True
    )

    time = models.IntegerField(
        _('Time'),
        choices=TIME_CHOICES,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True
        app_label = 'contact'
        verbose_name = _('Contact Request')
        verbose_name_plural = _('Contact Requests')

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @property
    def contact_details(self):
        return self.phone if self.contact_type == self.CONTACT_PHONE else self.email


class BaseContactRequestPlugin(AllinkBaseFormPlugin):

    # ContactRequestForm = get_class('contact.forms', 'ContactRequestForm')
    #
    # form_class = ContactRequestForm

    class Meta:
        app_label = 'contact'
        abstract = True

    def __str__(self):
        return 'Contact Request Form Plugin'
