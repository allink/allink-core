# -*- coding: utf-8 -*-
from django.db import models
from cms.models.fields import PageField
from cms.models.fields import PlaceholderField
from model_utils.fields import AutoCreatedField
from parler.models import TranslatedField
from filer.fields.image import FilerImageField
from djangocms_text_ckeditor.fields import HTMLField
from allink_core.core.models.fields import SortedM2MModelField

from allink_core.core.models import (
    AllinkCategoryFieldsModel,
    AllinkBaseTranslatableModel,
    AllinkBaseAppContentPlugin,
    AllinkBaseTranslatedFieldsModel,
    AllinkTimeFramedModel,
)
from allink_core.core.loading import get_class

AllinkNewsManager = get_class('news.managers', 'AllinkNewsManager')


class BaseNews(AllinkTimeFramedModel, AllinkCategoryFieldsModel, AllinkBaseTranslatableModel):
    TEASER_FIELD_FALLBACK_CONF = {
        'teaser_image': [
            {'model': 'self', 'field': 'teaser_image', },
            {'model': 'self', 'field': 'preview_image', },
        ],
        'teaser_title': [
            {'model': 'self', 'field': 'teaser_title', },
            {'model': 'self', 'field': 'title', },
        ],
        'teaser_technical_title': [
            {'model': 'self', 'field': 'teaser_technical_title', },
            {'model': 'self', 'field': 'entry_date', },
        ],
        'teaser_description': [
            {'model': 'self', 'field': 'teaser_description', },
            {'model': 'self', 'field': 'lead', },
        ],
        'teaser_link_text': [
            {'model': 'self', 'field': 'teaser_link_text', },
            {'model': 'self', 'field': 'TEASER_LINK_TEXT', },
        ],
        'teaser_link_url': [
            {'model': 'self', 'field': 'teaser_link_url', },
        ],
        # If you adjust this consider the possibility of adjusting the TEASER_FIELD_FALLBACK_CONF in AllinkTeaserMixin and other occurrences of TEASER_FIELD_FALLBACK_CONF!
    }

    slug_source_field_name = 'title'

    title = TranslatedField(any_language=True)
    entry_date = AutoCreatedField('Entry Date', editable=True)
    lead = TranslatedField()

    preview_image = FilerImageField(
        verbose_name='Preview Image',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_preview_image',
    )
    template = models.CharField(
        'Template',
        help_text='Choose a template.',
        max_length=50,
        blank=True,
        null=True,
    )

    header_placeholder = PlaceholderField('news_header', related_name='%(app_label)s_%(class)s_header_placeholder')
    content_placeholder = PlaceholderField('news_content', related_name='%(app_label)s_%(class)s_content_placeholder')

    objects = AllinkNewsManager()

    class Meta:
        abstract = True
        ordering = ('-entry_date',)
        app_label = 'news'
        verbose_name = 'News entry'
        verbose_name_plural = 'News'

    def __str__(self):
        return '%s - %s' % (self.title, self.entry_date.strftime('%d.%m.%Y %H:%M:%S'))


class BaseNewsTranslation(AllinkBaseTranslatedFieldsModel):
    master = models.ForeignKey(
        'news.News',
        on_delete=models.CASCADE,
        related_name='translations',
        null=True
    )
    title = models.CharField(
        max_length=255
    )
    lead = HTMLField(
        'Lead Text',
        help_text='Teaser text that in some cases is used in the list view and/or in the detail view.',
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
        app_label = 'news'


class BaseNewsAppContentPlugin(AllinkBaseAppContentPlugin):
    manual_entries = SortedM2MModelField(
        'news.News',
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
        related_name="load_more_internallink_news",
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        super(BaseNewsAppContentPlugin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'news'
