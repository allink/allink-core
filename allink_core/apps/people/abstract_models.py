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

from allink_core.core.models.fields import SortedM2MModelField
from allink_core.core.models import (
    AllinkCategoryFieldsModel,
    AllinkBaseTranslatableModel,
    AllinkBaseAppContentPlugin,
    AllinkContactFieldsModel,
    AllinkBaseTranslatedFieldsModel,
)
from allink_core.core.models.choices import SALUTATION_CHOICES
from allink_core.core.loading import get_class
from cms.models.fields import PageField


AllinkPeopleManager = get_class('people.managers', 'AllinkPeopleManager')


class BasePeople(SortableMixin, AllinkContactFieldsModel,
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
    lead = TranslatedField()
    company_name = models.CharField(
        _('Company Name'),
        max_length=255,
        blank=True,
        null=True
    )
    preview_image = FilerImageField(
        verbose_name='Preview Image',
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
        'people_header',
        related_name='%(app_label)s_%(class)s_header_placeholder'
    )
    content_placeholder = PlaceholderField(
        'people_content',
        related_name='%(app_label)s_%(class)s_content_placeholder'
    )
    street = models.CharField(
        _('Street'),
        max_length=255,
        blank=True,
        null=True
    )
    street_nr = models.CharField(
        _('Street Nr.'),
        max_length=50,
        blank=True,
        null=True
    )
    street_additional = models.CharField(
        _('Address Additional'),
        max_length=255,
        blank=True,
        null=True
    )
    zip_code = models.CharField(
        _('Zip Code'),
        max_length=10,
        blank=True,
        null=True
    )
    place = models.CharField(
        _('Place'),
        max_length=255,
        blank=True,
        null=True
    )
    country = TranslatedField()

    objects = AllinkPeopleManager()

    class Meta:
        abstract = True
        app_label = 'people'
        ordering = 'sort_order',
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    def __str__(self):
        return '%s - %s' % (self.full_name, self.created.strftime('%d.%m.%Y'))

    @cached_property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @cached_property
    def title(self):
        return '{} {}'.format(self.first_name, self.last_name)

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
    job_function = models.CharField(
        'Function',
        max_length=255,
        blank=True,
        null=True,
    )
    lead = HTMLField(
        'Lead Text',
        help_text=('Teaser text that in some cases is used in the list view '
                   'and/or in the detail view.'),
        blank=True,
        null=True,
    )
    country = models.CharField(
        'Country',
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True
        app_label = 'people'


class BasePeopleAppContentPlugin(AllinkBaseAppContentPlugin):
    manual_entries = SortedM2MModelField(
        'people.People',
        blank=True,
        help_text=('Select and arrange specific entries, or, leave blank to select all. (If '
                   'manual entries are selected the category filtering will be applied as well.)')
    )
    apphook_page = PageField(
        verbose_name='Apphook Page',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text='If provided, this Apphook-Page will be used to generate the detail link.',
    )
    load_more_internallink = PageField(
        verbose_name='Custom Load More Link',
        help_text='Link for Button Below Items if custom URL is chosen',
        related_name="load_more_internallink_people",
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
        app_label = 'people'

    def save(self, *args, **kwargs):
        super(BasePeopleAppContentPlugin, self).save(*args, **kwargs)
