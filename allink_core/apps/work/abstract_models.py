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
from allink_core.core.loading import get_class
from allink_core.core.models import (
    AllinkCategoryFieldsModel,
    AllinkBaseTranslatableModel,
    AllinkBaseAppContentPlugin,
    AllinkBaseSearchPlugin,
    AllinkBaseTranslatedFieldsModel,
)

AllinkWorkManager = get_class('work.managers', 'AllinkWorkManager')


class BaseWork(SortableMixin, AllinkCategoryFieldsModel, AllinkBaseTranslatableModel):
    slug_source_field_name = 'title'

    title = TranslatedField(any_language=True)
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
        u'work_header',
        related_name='%(app_label)s_%(class)s_header_placeholder'
    )
    content_placeholder = PlaceholderField(
        u'work_content',
        related_name='%(app_label)s_%(class)s_content_placeholder'
    )

    objects = AllinkWorkManager()

    class Meta:
        abstract = True
        app_label = 'work'
        ordering = ('sort_order',)
        verbose_name = _('Project / Reference')
        verbose_name_plural = _('Projects / References')

    def __str__(self):
        return u'%s - %s' % (self.title, self.created.strftime('%d.%m.%Y'))


class BaseWorkTranslation(AllinkBaseTranslatedFieldsModel):
    master = models.ForeignKey(
        'work.Work',
        on_delete=models.CASCADE,
        related_name='translations',
        null=True
    )
    title = models.CharField(
        max_length=255
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

    class Meta:
        abstract = True
        app_label = 'work'


class BaseWorkAppContentPlugin(AllinkBaseAppContentPlugin):

    manual_entries = SortedM2MModelField(
        'work.Work',
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

    def save(self, *args, **kwargs):
        super(BaseWorkAppContentPlugin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'work'


class BaseWorkSearchPlugin(AllinkBaseSearchPlugin):

    class Meta:
        abstract = True
        app_label = 'work'
