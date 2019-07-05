# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models

from cms.models.fields import PageField
from cms.models.fields import PlaceholderField
from adminsortable.models import SortableMixin
from parler.models import TranslatedField
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField
from django.utils.functional import cached_property

from aldryn_common.admin_fields.sortedm2m import SortedM2MModelField
from allink_core.core.models import (
    AllinkCategoryFieldsModel,
    AllinkBaseTranslatableModel,
    AllinkBaseAppContentPlugin,
    AllinkContactFieldsModel,
    AllinkAddressFieldsModel,
    AllinkBaseTranslatedFieldsModel,
)
from allink_core.core.models.choices import SALUTATION_CHOICES
from allink_core.core.loading import get_class


AllinkPeopleManager = get_class('people.managers', 'AllinkPeopleManager')


class BasePeople(SortableMixin, AllinkContactFieldsModel, AllinkAddressFieldsModel,
                 AllinkCategoryFieldsModel, AllinkBaseTranslatableModel):
    slug_source_field_name = 'full_name'

    salutation = models.IntegerField(
        _('Salutation'),
        choices=SALUTATION_CHOICES,
        null=True
    )
    first_name = models.CharField(
        _('First Name'),
        max_length=255
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=255
    )
    slug = TranslatedField(any_language=True)
    lead = TranslatedField()
    company_name = models.CharField(
        _('Company Name'),
        max_length=255,
        blank=True,
        null=True
    )
    preview_image = FilerImageField(
        verbose_name=_('Preview Image'),
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_preview_image',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True
    )
    header_placeholder = PlaceholderField(
        u'people_header',
        related_name='%(app_label)s_%(class)s_header_placeholder'
    )
    content_placeholder = PlaceholderField(
        u'people_content',
        related_name='%(app_label)s_%(class)s_content_placeholder'
    )

    objects = AllinkPeopleManager()

    class Meta:
        abstract = True
        app_label = 'people'
        ordering = ('sort_order',)
        verbose_name = _('Person')
        verbose_name_plural = _('People')

    def __str__(self):
        return u'%s - %s' % (self.full_name, self.created.strftime('%d.%m.%Y'))

    @cached_property
    def full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @cached_property
    def title(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @cached_property
    def units(self):
        units = []
        for unit in self.categories.filter(identifier='units'):
            units.append(unit.name)
        return ','.join(units)


class BasePeopleTranslation(AllinkBaseTranslatedFieldsModel):
    master = models.ForeignKey(
        'people.People',
        on_delete=models.CASCADE,
        related_name='translations',
        null=True
    )
    slug = models.SlugField(
        _('Slug'),
        max_length=255,
        default='',
        blank=True,
        help_text=_('Leave blank to auto-generate a unique slug.')
    )
    job_function = models.CharField(
        _('Function'),
        max_length=255,
        blank=True,
        null=True,
    )
    lead = HTMLField(
        _('Lead Text'),
        help_text=_('Teaser text that in some cases is used in the list view '
                    u'and/or in the detail view.'),
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
        app_label = 'people'


class BasePeopleAppContentPlugin(AllinkBaseAppContentPlugin):
    manual_entries = SortedM2MModelField(
        'people.People',
        blank=True,
        help_text=_('Select and arrange specific entries, or, leave blank to select all. (If '
                    'manual entries are selected the category filtering will be ignored.)')
    )
    apphook_page = PageField(
        verbose_name=_('Apphook Page'),
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text=_('If provided, this Apphook-Page will be used to generate the detail link.'),
    )

    class Meta:
        abstract = True
        app_label = 'people'

    def save(self, *args, **kwargs):
        super(BasePeopleAppContentPlugin, self).save(*args, **kwargs)
