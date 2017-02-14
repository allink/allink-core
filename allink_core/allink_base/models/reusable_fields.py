# -*- coding: utf-8 -*-
import phonenumbers
from urlparse import urlparse
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from cms.models.fields import PageField
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from phonenumber_field.modelfields import PhoneNumberField

from djangocms_attributes_field.fields import AttributesField

from .choices import SPECIAL_LINKS_CHOICES


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


class AllinkLinkFieldsModel(models.Model):
    link_url = models.URLField(
        verbose_name=(u'External link'),
        blank=True,
        default='',
        help_text=_(u'Provide a valid URL to an external website.'),
    )
    link_page = PageField(
        verbose_name=_(u'Internal link'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text=_(u'If provided, overrides the external link.'),
    )
    link_mailto = models.EmailField(
        verbose_name=_(u'Email address'),
        blank=True,
        null=True,
        max_length=255,
    )
    link_phone = models.CharField(
        verbose_name=_(u'Phone'),
        blank=True,
        null=True,
        max_length=255,
    )
    link_anchor = models.CharField(
        verbose_name=_(u'Anchor'),
        max_length=255,
        blank=True,
        help_text=_(u'Appends the value only after the internal or external link. '
                    u'Do <em>not</em> include a preceding "#" symbol.'),
    )
    link_target = models.BooleanField(
        verbose_name=_(u'Open in new Window'),
        blank=True,
    )
    link_file = FilerFileField(
        verbose_name=_(u'file'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    link_special = models.CharField(
        verbose_name=_(u'Special Links'),
        choices=SPECIAL_LINKS_CHOICES,
        max_length=255,
        blank=True,
        null=True
    )
    link_attributes = AttributesField(
        verbose_name=_(u'Attributes'),
        blank=True,
        excluded_keys=['class', 'href', 'target'],
    )

    class Meta:
        abstract = True

    def get_link_url(self):
        if self.link_page_id:
            link = self.link_page.get_absolute_url()
        elif self.link_url:
            link = self.link_url
        elif self.link_phone:
            link = 'tel:{}'.format(self.link_phone.replace(' ', ''))
        elif self.link_mailto:
            link = 'mailto:{}'.format(self.link_mailto)
        elif self.link_file:
            link = self.link_file.url
        elif self.link_special:
            link = reverse(self.link_special)
        else:
            link = ''
        if self.link_anchor:
            link += '#{}'.format(self.link_anchor)
        return link

    def clean(self):
        super(AllinkLinkFieldsModel, self).clean()
        field_names = (
            'link_url',
            'link_page',
            'link_mailto',
            'link_phone',
            'link_file',
        )
        anchor_field_name = 'link_anchor'
        field_names_allowed_with_anchor = (
            'link_url',
            'link_page',
            'link_file',
        )

        anchor_field_verbose_name = force_text(
           self._meta.get_field_by_name(anchor_field_name)[0].verbose_name)
        anchor_field_value = getattr(self, anchor_field_name)

        link_fields = {
            key: getattr(self, key)
            for key in field_names
        }
        link_field_verbose_names = {
            key: force_text(self._meta.get_field_by_name(key)[0].verbose_name)
            for key in link_fields.keys()
        }
        provided_link_fields = {
            key: value
            for key, value in link_fields.items()
            if value
        }
        if len(provided_link_fields) > 1:
            # Too many fields have a value.
            verbose_names = sorted(link_field_verbose_names.values())
            error_msg = _('Only one of %s or %s may be given.') % (
                ', '.join(verbose_names[:-1]),
                verbose_names[-1],
            )
            errors = {}.fromkeys(provided_link_fields.keys(), error_msg)
            raise ValidationError(errors)

        if anchor_field_value:
            for field_name in provided_link_fields.keys():
                if field_name not in field_names_allowed_with_anchor:
                    error_msg = _('%(anchor_field_verbose_name)s is not allowed together with %(field_name)s') % {
                        'anchor_field_verbose_name': anchor_field_verbose_name,
                        'field_name': link_field_verbose_names.get(field_name)
                    }
                    raise ValidationError({
                        anchor_field_name: error_msg,
                        field_name: error_msg,
                    })
