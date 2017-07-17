# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models

from allink_core.core.loading import get_model
from allink_core.core.models.models import AllinkSimpleRegistrationFieldsModel, AllinkBaseFormPlugin


class BaseContactRequest(AllinkSimpleRegistrationFieldsModel):
    TIME_CHOICES = (
        (None, _(u'-- between --')),
        (1, u'09:00-11:00'),
        (2, u'13:00-15:00'),
        (3, u'15:00-17:00'),
    )
    CONTACT_PHONE = 10
    CONTACT_EMAIL = 20

    CONTACT_CHOICES = (
        (None, _(u'-- please choose --')),
        (CONTACT_PHONE, _(u'Phone')),
        (CONTACT_EMAIL, _(u'Email')),
    )

    contact_type = models.IntegerField(
        _(u'Please contact me via'),
        choices=CONTACT_CHOICES,
    )

    date = models.DateField(
        _(u'Date'),
        blank=True,
        null=True
    )

    time = models.IntegerField(
        _(u'Time'),
        choices=TIME_CHOICES,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @property
    def contact_details(self):
        return self.phone if self.contact_type == self.CONTACT_PHONE else self.email

    @classmethod
    def get_verbose_name(cls):
        Config = get_model('config', 'Config')
        try:
            field_name = cls._meta.model_name + '_verbose'
            return getattr(Config.get_solo(), field_name)
        except:
            return cls._meta.verbose_name

    @classmethod
    def get_verbose_name_plural(cls):
        Config = get_model('config', 'Config')
        try:
            field_name = cls._meta.model_name + '_verbose_plural'
            return getattr(Config.get_solo(), field_name)
        except:
            return cls._meta.verbose_name_plural

    class Meta:
        abstract = True
        verbose_name = _(u'Contact Request')
        verbose_name_plural = _(u'Contact Requests')


class BaseContactRequestPlugin(AllinkBaseFormPlugin):

    # ContactRequestForm = get_class('contact.forms', 'ContactRequestForm')
    #
    # form_class = ContactRequestForm

    class Meta:
        abstract = True

    def __str__(self):
        return 'Contact Request Form Plugin'
