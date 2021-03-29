# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models

from cms.models.fields import PageField
from cms.models.fields import PlaceholderField
from adminsortable.models import SortableMixin
from parler.models import TranslatedField
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

from allink_core.core.models.fields import SortedM2MModelField
from allink_core.core.models import (
    AllinkCategoryFieldsModel,
    AllinkBaseTranslatableModel,
    AllinkBaseAppContentPlugin,
    AllinkBaseTranslatedFieldsModel,
)

from .managers import DummyAppManager


class DummyApp(SortableMixin, AllinkCategoryFieldsModel, AllinkBaseTranslatableModel):
    slug_source_field_name = 'title'

    title = TranslatedField(any_language=True)
    lead = TranslatedField()

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
        'dummy_app_header',
        related_name='%(app_label)s_%(class)s_header_placeholder'
    )
    content_placeholder = PlaceholderField(
        'dummy_app_content',
        related_name='%(app_label)s_%(class)s_content_placeholder'
    )

    objects = DummyAppManager()

    class Meta:
        app_label = 'dummy_app'
        ordering = ('sort_order',)
        verbose_name = 'DummyApp'
        verbose_name_plural = 'DummyApp'

    def __str__(self):
        return self.title


class DummyAppTranslation(AllinkBaseTranslatedFieldsModel):
    master = models.ForeignKey(
        'dummy_app.DummyApp',
        on_delete=models.CASCADE,
        related_name='translations',
        null=True
    )

    title = models.CharField(
        max_length=255
    )
    lead = HTMLField(
        _('Lead Text'),
        help_text='Teaser text that in some cases is used in the list view and/or in the detail view.',
        blank=True,
        null=True,
    )

    class Meta:
        app_label = 'dummy_app'


class DummyAppAppContentPlugin(AllinkBaseAppContentPlugin):
    data_model = DummyApp

    manual_entries = SortedM2MModelField(
        'dummy_app.DummyApp',
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
        related_name="load_more_internallink_dummy_app",
        blank=True,
        null=True,
    )

    class Meta:
        app_label = 'dummy_app'
