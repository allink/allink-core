# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models

from cms.models.fields import PageField
from cms.models.fields import PlaceholderField
from adminsortable.models import SortableMixin
from parler.models import TranslatedField
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

from aldryn_common.admin_fields.sortedm2m import SortedM2MModelField
from allink_core.core.models import (
    AllinkCategoryFieldsModel,
    AllinkBaseTranslatableModel,
    AllinkBaseAppContentPlugin,
    AllinkBaseTranslatedFieldsModel,
)
from allink_core.core.loading import get_class

AllinkTestimonialsManager = get_class('testimonials.managers', 'AllinkTestimonialsManager')


class BaseTestimonials(SortableMixin, AllinkCategoryFieldsModel, AllinkBaseTranslatableModel):
    slug_source_field_name = 'full_name'

    first_name = models.CharField(
        _('First Name'),
        max_length=255,
        default=''
    )
    last_name = models.CharField(
        _('Last Name'),
        max_length=255,
        default=''
    )
    slug = TranslatedField(any_language=True)
    lead = TranslatedField()
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
        'testimonials_header',
        related_name='%(app_label)s_%(class)s_header_placeholder'
    )
    content_placeholder = PlaceholderField(
        'testimonials_content',
        related_name='%(app_label)s_%(class)s_content_placeholder'
    )
    company_name = models.CharField(
        _('Company Name'),
        max_length=255,
        blank=True,
        null=True
    )

    objects = AllinkTestimonialsManager()

    class Meta:
        abstract = True
        app_label = 'testimonials'
        ordering = ('sort_order',)
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')

    def __str__(self):
        return '%s - %s' % (self.full_name, self.created.strftime('%d.%m.%Y'))

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def title(self):
        return '{} {}'.format(self.first_name, self.last_name)


class BaseTestimonialsTranslation(AllinkBaseTranslatedFieldsModel):
    master = models.ForeignKey(
        'testimonials.Testimonials',
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
    lead = HTMLField(
        _('Lead Text'),
        help_text=_('Teaser text that in some cases is used in the list view and/or in the detail view.'),
        blank=True,
        null=True,
    )
    job_function = models.CharField(
        _('Function'),
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
        app_label = 'testimonials'


class BaseTestimonialsAppContentPlugin(AllinkBaseAppContentPlugin):
    manual_entries = SortedM2MModelField(
        'testimonials.Testimonials',
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
        app_label = 'testimonials'

    def save(self, *args, **kwargs):
        super(BaseTestimonialsAppContentPlugin, self).save(*args, **kwargs)
