# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.utils.functional import cached_property

from cms.models.fields import PlaceholderField
from adminsortable.models import SortableMixin
from parler.models import TranslatableModel, TranslatedField, TranslatedFieldsModel
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField
from django.utils.functional import cached_property

from aldryn_translation_tools.models import TranslationHelperMixin
from aldryn_common.admin_fields.sortedm2m import SortedM2MModelField
from allink_core.core.models.models import AllinkBaseAppContentPlugin, AllinkBaseModel, AllinkContactFieldsModel, AllinkAddressFieldsModel, AllinkBaseTranslatedFieldsModel
from allink_core.core.models.mixins import AllinkTranslatedAutoSlugifyMixin
from allink_core.core.models.choices import SALUTATION_CHOICES
from allink_core.core.loading import get_model

from allink_core.apps.people.managers import AllinkPeopleManager


class BasePeople(SortableMixin, TranslationHelperMixin, AllinkTranslatedAutoSlugifyMixin, TranslatableModel, AllinkContactFieldsModel, AllinkAddressFieldsModel, AllinkBaseModel):
    slug_source_field_name = 'full_name'

    salutation = models.IntegerField(
        _(u'Salutation'),
        choices=SALUTATION_CHOICES,
        null=True
    )
    first_name = models.CharField(
        _(u'First Name'),
        max_length=255
    )
    last_name = models.CharField(
        _(u'Last Name'),
        max_length=255
    )

    slug = TranslatedField(any_language=True)
    lead = TranslatedField()

    company_name = models.CharField(
        _(u'Company Name'),
        max_length=255,
        blank=True,
        null=True
    )
    preview_image = FilerImageField(
        verbose_name=_(u'Preview Image'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_preview_image',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True
    )

    header_placeholder = PlaceholderField(u'people_header', related_name='%(app_label)s_%(class)s_header_placeholder')
    content_placeholder = PlaceholderField(u'people_content', related_name='%(app_label)s_%(class)s_content_placeholder')

    objects = AllinkPeopleManager()

    class Meta:
        abstract = True
        app_label = 'people'
        ordering = ('sort_order',)
        verbose_name = _('Person')
        verbose_name_plural = _('People')

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
    master = models.ForeignKey('people.People', related_name='translations', null=True)

    slug = models.SlugField(
        _(u'Slug'),
        max_length=255,
        default='',
        blank=True,
        help_text=_(u'Leave blank to auto-generate a unique slug.')
    )
    job_function = models.CharField(
        _(u'Function'),
        max_length=255,
        blank=True,
        null=True,
    )

    lead = HTMLField(
        _(u'Lead Text'),
        help_text=_(u'Teaser text that in some cases is used in the list view and/or in the detail view.'),
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

    def save(self, *args, **kwargs):
        super(BasePeopleAppContentPlugin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'people'
