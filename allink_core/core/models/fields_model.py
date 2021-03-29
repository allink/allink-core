# -*- coding: utf-8 -*-
from urllib.parse import urlparse
import phonenumbers
from importlib import import_module

from django.conf import settings
from django.db import models
from django.urls import NoReverseMatch
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from djangocms_attributes_field.fields import AttributesField
from cms.models.fields import PageField
from allink_core.core.loading import get_model
from allink_core.core.models.choices import (
    SALUTATION_CHOICES, TARGET_CHOICES, NEW_WINDOW, SOFTPAGE, FORM_MODAL, IMAGE_MODAL, DEFAULT_MODAL, BLANK_CHOICE, )
from allink_core.core_apps.allink_categories.models import AllinkCategory
from allink_core.core.models.managers import AllinkCategoryModelManager
from allink_core.core.utils import get_additional_choices


__all__ = [
    'AllinkStatusFieldsModel',
    'AllinkTimeFramedModel',
    'AllinkCategoryFieldsModel',
    'AllinkSEOFieldsModel',
    'AllinkSEOTranslatedFieldsModel',
    'AllinkTeaserFieldsModel',
    'AllinkTeaserTranslatedFieldsModel',
    'AllinkContactFieldsModel',
    'AllinkInternalLinkFieldsModel',
    'AllinkLinkFieldsModel',
    'AllinkSimpleRegistrationFieldsModel',
]


class AllinkStatusFieldsModel(models.Model):
    """
    Base class for status field

    hint: Just override STATUS_CHOICES or STATUS_DEFAULT in you model, if needed.
    """
    ACTIVE = 1
    INACTIVE = 2
    STATUS_DEFAULT = ACTIVE

    STATUS_CHOICES = [
        (ACTIVE, 'active'),
        (INACTIVE, 'inactive')
    ]
    status = models.IntegerField('status', choices=STATUS_CHOICES, default=STATUS_DEFAULT)

    class Meta:
        abstract = True


class AllinkTimeFramedModel(models.Model):
    """
    Base class for timeframed models
    We don't use django_modelutils, because they add a timeframed default manager.
    And this is not compatible with parler's TranslatableQuerySet.

    """
    start = models.DateTimeField('start', null=True, blank=True)
    end = models.DateTimeField('end', null=True, blank=True)

    class Meta:
        abstract = True


class AllinkCategoryFieldsModel(models.Model):
    """
    Base class for apps with categories
    """
    categories = models.ManyToManyField(
        AllinkCategory,
        blank=True
    )

    objects = AllinkCategoryModelManager()

    class Meta:
        abstract = True

    @cached_property
    def fetch_categories(self):
        return self.categories.all()

    @classmethod
    def get_relevant_categories(cls):
        """
        returns a queryset of all relevant categories for a the model_name
        """
        result = AllinkCategory.objects.none()
        for root in AllinkCategory.get_root_nodes().filter(model_names__contains=[cls._meta.model_name]):
            result |= root.get_descendants()
        return result

    @classmethod
    def get_can_have_categories(cls):
        return cls._meta.model_name in dict(settings.PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES)


class AllinkSEOFieldsModel(models.Model):
    """
    Base class for all non translated SEO fields
    """
    og_image = FilerImageField(
        verbose_name='og:Image',
        on_delete=models.PROTECT,
        help_text=
            'og: image is used when shared on Facebook/ Twitter etc. (Min. 1200 x 630 px)<br>'
            'Page: 1. fallback is teaser_image, 2. fallback is field allink_config.default_og_image.<br>'
            'App: 1. fallback = preview_image 2. fallback is teaser_image, 3. '
            'fallback is defined in allink_config.default_og_image.<br>',
        related_name='%(app_label)s_%(class)s_og_image',
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class AllinkSEOTranslatedFieldsModel(models.Model):
    """
    Base class for all translated SEO fields

    This is supposed to be used in combination with TranslatedFieldsModel
    e.g.: ...(AllinkSEOTranslatedFieldsModel, TranslatedFieldsModel)
    """
    og_title = models.CharField(
        verbose_name='og:title | <title> Tag',
        max_length=255,
        help_text='title-tag is used when shared on Facebook/ Twitter etc.<br>'
                  'Also used to overwrite "meta property="og:image.."" and title-tag<br>'
                  'Page: fallback is field "title" of the page.<br>'
                  'App: fallback is field "title".',
        blank=True,
        default=''
    )
    og_description = models.TextField(
        verbose_name='og:description | meta description',
        max_length=255,
        help_text='Description is used when shared on Facebook/ Twitter etc.<br>'
                  'Also used to overwrite  "meta" property="og:description" .. and "meta name="description"<br>'
                  'Page: fallback is field "teaser_description" of the page, if set. Otherwise empty.<br>'
                  'App: fallback is field "lead", if set. Otherwise empty.',
        blank=True,
        default=''
    )

    class Meta:
        abstract = True


class AllinkTeaserFieldsModel(models.Model):
    """
    Base class for all teaser fields

    use this together with: AllinkTeaserMixin
    """
    teaser_image = FilerImageField(
        verbose_name='Teaser image',
        on_delete=models.PROTECT,
        help_text=
            'Optional field for teaser image. og: properties are used when shared on Facebook/ Twitter etc. '
            '(Min. 1200 x 630 px)<br>'
            'Also used as "meta" property="og:image"<br>'
            'Page: 1. fallback is allink_config.default_og_image.<br>'
            'App: 1. fallback = preview_image 2. fallback is defined in allink_config.default_og_image.<br>',
        related_name='%(app_label)s_%(class)s_teaser_image',
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class AllinkTeaserTranslatedFieldsModel(models.Model):
    """
    This is supposed to be used in combination with TranslatedFieldsModel
    e.g.: ...(AllinkTeaserTranslatedFieldsModel, TranslatedFieldsModel)

    use this together with: AllinkTeaserMixin
    """
    teaser_title = models.CharField(
        'Teaser title',
        help_text='Page: fallback is field "title" of the page.<br>'
                  'App: fallback is field "title".',
        max_length=255,
        blank=True,
        default=''
    )
    teaser_technical_title = models.CharField(
        'Teaser technical title',
        help_text='Page: no fallback.<br>'
                  'App: fallback is hardcoded per app in the teaser_dict.',
        max_length=255,
        blank=True,
        default=''
    )
    teaser_description = models.TextField(
        'Teaser description',
        help_text='Page: no fallback.<br>'
                  'App: fallback is field "lead".'
                  'Please only use 80 to 120 characters. Best results will be achieved with around 100 characters.',
        blank=True,
        default=''
    )
    teaser_link_text = models.CharField(
        'Teaser link text',
        help_text='Page: no fallback.<br>'
                  'App: fallback is hardcoded per app in the teaser_dict.',
        max_length=255,
        blank=True,
        default=''
    )

    teaser_link_url = models.URLField(
        verbose_name='External link',
        blank=True,
        null=True,
        help_text='Provide a valid URL to an external website.',
        max_length=500,
    )

    class Meta:
        abstract = True


class AllinkContactFieldsModel(models.Model):
    """
    Base class for all contact fields
    """
    phone = PhoneNumberField(
        _('Phone'),
        help_text=_(
            'We automatically handle phone number formatting, '
            'Please provide the number in the following format "+41 43 123 45 67".'),
        blank=True,
        null=True
    )
    mobile = PhoneNumberField(
        _('Mobile'),
        help_text=_(
            'We automatically handle phone number formatting, '
            'Please provide the number in the following format "+41 43 123 45 67".'),
        blank=True,
        null=True
    )
    fax = PhoneNumberField(
        _('Fax'),
        help_text=_(
            'We automatically handle phone number formatting, '
            'Please provide the number in the following format "+41 43 123 45 67".'),
        blank=True,
        null=True
    )
    email = models.EmailField(
        _('Email'),
        blank=True,
        default=''
    )
    website = models.URLField(
        _('Website'),
        blank=True,
        null=True
    )

    class Meta:
        abstract = True

    @cached_property
    def phone_formatted(self):
        if self.phone:
            x = phonenumbers.parse(str(self.phone), None)
            return str(phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL))

    @cached_property
    def mobile_formatted(self):
        if self.mobile:
            x = phonenumbers.parse(str(self.mobile), None)
            return str(phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL))

    @cached_property
    def fax_formatted(self):
        if self.fax:
            x = phonenumbers.parse(str(self.fax), None)
            return str(phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL))

    @cached_property
    def website_clean(self):
        if self.website:
            website = urlparse(self.website)
            domain = '{uri.netloc}'.format(uri=website)
            return domain.replace('www.', '')


class AllinkInternalLinkFieldsModel(models.Model):
    """
    Base class for all internal link related fields
    """
    #  Page redirect
    link_page = PageField(
        verbose_name='New Page',
        null=True,
        on_delete=models.PROTECT,
        help_text='If provided, overrides the external link and New Apphook-Page.',
    )
    #  Fields for app redirect
    link_apphook_page = PageField(
        verbose_name='New Apphook-Page',
        null=True,
        on_delete=models.PROTECT,
        help_text='If provided, overrides the external link.',
        related_name='%(app_label)s_%(class)s_app_legacy_redirects'
    )
    link_object_id = models.IntegerField(
        null=True,
        help_text='To which object directs the url.'
    )
    link_model = models.CharField(
        null=True,
        max_length=300,
        help_text='Dotted Path to referenced Model'
    )
    link_url_name = models.CharField(
        null=True,
        max_length=64,
        help_text='Name of the App-URL to use.'
    )
    link_url_kwargs = ArrayField(
        models.CharField(
            max_length=50,
            blank=True,
            null=True
        ),
        blank=True,
        null=True,
        help_text='Keyword arguments used to reverse url.'
    )

    class Meta:
        abstract = True

    @cached_property
    def link(self):
        if self.link_page:
            link = self.link_page.get_absolute_url()
        elif self.link_apphook_page:
            try:
                obj_model = get_model(self.link_model.split('.')[-3], self.link_model.split('.')[-1])
                obj = obj_model.objects.get(id=self.link_object_id)
                url_kwargs = {key: getattr(obj, key) for key in self.link_url_kwargs}
                url_name = '{}:{}'.format(self.link_apphook_page.application_namespace, self.link_url_name)
                link = reverse(url_name, kwargs=url_kwargs)
            except KeyError:
                link = ''
        else:
            link = ''
        return link

    @cached_property
    def link_object(self):
        if self.link_page:
            link_obj = self.link_page
        elif self.link_apphook_page:
            try:
                obj_module = import_module('.'.join(self.link_model.split('.')[:-1]))
                obj_model = getattr(obj_module, self.link_model.split('.')[-1])
                link_obj = obj_model.objects.get(id=self.link_object_id)
            except KeyError:
                link_obj = None
        else:
            link_obj = None
        return link_obj

    @cached_property
    def is_page_link(self):
        if self.link_page:
            return True
        else:
            return False


class AllinkLinkFieldsModel(AllinkInternalLinkFieldsModel):
    """
    Base class for all the link related fields (including internal link fields)
    """
    link_url = models.URLField(
        verbose_name='External link',
        blank=True,
        default='',
        help_text='Provide a valid URL to an external website.',
        max_length=500,
    )
    link_mailto = models.EmailField(
        verbose_name='Email address',
        blank=True,
        null=True,
        max_length=255,
    )
    link_phone = models.CharField(
        verbose_name='Phone',
        blank=True,
        null=True,
        max_length=255,
    )
    link_anchor = models.CharField(
        verbose_name='Anchor',
        max_length=255,
        blank=True,
        help_text='Appends the value only after the internal or external link.<br>'
                    'Do <strong>not</strong> include a preceding "#" symbol.',
    )
    link_target = models.IntegerField(
        'Link Target',
        choices=TARGET_CHOICES,
        null=True,
        blank=True
    )
    link_file = FilerFileField(
        verbose_name='file',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    link_special = models.CharField(
        verbose_name='Special Links',
        max_length=255,
        blank=True,
        null=True
    )
    link_attributes = AttributesField(
        verbose_name='Attributes',
        blank=True,
        excluded_keys=['class', 'href', 'target'],
    )

    class Meta:
        abstract = True

    @cached_property
    def new_window_enabled(self):
        return True if self.link_target == NEW_WINDOW and not self.form_modal_enabled \
                       and not self.softpage_enabled else False

    @cached_property
    def softpage_enabled(self):
        return True if self.link_target == SOFTPAGE else False

    @cached_property
    def form_modal_enabled(self):
        return True if self.link_target == FORM_MODAL else False

    @cached_property
    def image_modal_enabled(self):
        return True if self.link_target == IMAGE_MODAL else False

    @property
    def default_modal_enabled(self):
        return True if self.link_target == DEFAULT_MODAL else False

    @classmethod
    def get_link_special_choices(self):
        return BLANK_CHOICE + get_additional_choices('BUTTON_LINK_SPECIAL_LINKS_CHOICES')

    @cached_property
    def link_url_typed(self):
        internal_link = self.link
        if internal_link:
            link = internal_link
        elif self.link_url:
            link = self.link_url
        elif self.link_phone:
            link = 'tel:{}'.format(self.link_phone.replace(' ', ''))
        elif self.link_mailto:
            link = 'mailto:{}'.format(self.link_mailto)
        elif self.link_file:
            link = self.link_file.url
        elif self.link_special:
            try:
                """
                because we are always in a plugin (e.g Button, Image..)
                and plugins can appear more than once on the same page,
                the urls should always pass a plugin_id (not all urls do at the moment)
                """
                link = reverse(self.link_special, kwargs={'plugin_id': self.id})
            except NoReverseMatch:
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
            'link_apphook_page',
            'link_mailto',
            'link_phone',
            'link_file',
        )
        anchor_field_name = 'link_anchor'
        field_names_allowed_with_anchor = (
            'link_url',
            'link_page',
            'link_apphook_page',
            'link_file',
        )

        anchor_field_verbose_name = force_text(self._meta.get_field(anchor_field_name).verbose_name)
        anchor_field_value = getattr(self, anchor_field_name)

        link_fields = {
            key: getattr(self, key)
            for key in field_names
        }
        link_field_verbose_names = {
            key: force_text(self._meta.get_field(key).verbose_name)
            for key in link_fields.keys()
        }
        provided_link_fields = {
            key: value
            for key, value in link_fields.items()
            if value
        }

        if anchor_field_value:
            for field_name in provided_link_fields.keys():
                if field_name not in field_names_allowed_with_anchor:
                    error_msg = '%(anchor_field_verbose_name)s is not allowed together with %(field_name)s' % {
                        'anchor_field_verbose_name': anchor_field_verbose_name,
                        'field_name': link_field_verbose_names.get(field_name)
                    }
                    raise ValidationError({
                        anchor_field_name: error_msg,
                        field_name: error_msg,
                    })


class AllinkSimpleRegistrationFieldsModel(TimeStampedModel):
    """
    Base class for all registration related fields
    """
    salutation = models.IntegerField(
        _('Salutation'),
        choices=SALUTATION_CHOICES,
        null=True
    )

    first_name = models.CharField(
        _('First Name'),
        max_length=255,
        null=True
    )

    last_name = models.CharField(
        _('Last Name'),
        max_length=255,
        null=True
    )

    email = models.EmailField(
        _('Email'),
        null=True
    )

    company_name = models.CharField(
        _('Company'),
        max_length=255,
        blank=True,
        null=True
    )
    phone = models.CharField(
        _('Phone'),
        max_length=30,
        blank=True,
        null=True
    )

    message = models.TextField(
        _('Message'),
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True
