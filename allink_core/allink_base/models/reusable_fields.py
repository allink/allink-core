# -*- coding: utf-8 -*-
import phonenumbers
from urlparse import urlparse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField
from phonenumber_field.modelfields import PhoneNumberField


class AllinkContactFieldsModel(models.Model):

    class Meta:
        abstract = True

    phone = PhoneNumberField(
        _(u'Phone'),
        help_text=_(u'Required Format: +41 41 345 67 89'),
        blank=True,
        null=True
    )
    mobile = PhoneNumberField(
        _(u'Mobile'),
        help_text=_(u'Required Format: +41 41 345 67 89'),
        blank=True,
        null=True
    )
    fax = PhoneNumberField(
        _(u'Fax'),
        help_text=_(u'Required Format: +41 41 345 67 89'),
        blank=True,
        null=True
    )
    email = models.EmailField(
        _(u'Email'),
        blank=True,
        default=''
    )
    website = models.URLField(
        _(u'Website'),
        blank=True,
        null=True
    )

    @property
    def phone_formatted(self):
        if self.phone:
            x = phonenumbers.parse(str(self.phone), None)
            return (str(phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL)))

    @property
    def mobile_formatted(self):
        if self.mobile:
            x = phonenumbers.parse(str(self.mobile), None)
            return (str(phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL)))

    @property
    def fax_formatted(self):
        if self.fax:
            x = phonenumbers.parse(str(self.fax), None)
            return (str(phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL)))

    @property
    def website_clean(self):
        if self.website:
            website = urlparse(self.website)
            domain = '{uri.netloc}'.format(uri=website)
            return domain.replace('www.', '')


class AllinkMetaTagFieldsModel(models.Model):

    class Meta:
        abstract = True

    og_image = FilerImageField(
        verbose_name=_(u'og:Image'),
        help_text=_(u'Preview image when page/post is shared on Facebook. <br>Min. 1200 x 630 for best results.'),
        blank=True,
        null=True
    )

    og_title = models.CharField(
        verbose_name=_(u'og:title'),
        max_length=255,
        help_text=_(u'Title when shared on Facebook.'),
        blank=True,
        null=True
    )

    og_description = models.CharField(
        verbose_name=_(u'og:description'),
        max_length=255,
        help_text=_(u'Description when shared on Facebook.'),
        blank=True,
        null=True
    )
