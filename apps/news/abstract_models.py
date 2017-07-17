# -*- coding: utf-8 -*-
import datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from model_utils.models import TimeFramedModel
from parler.models import TranslatableModel, TranslatedField
from filer.fields.image import FilerImageField
from djangocms_text_ckeditor.fields import HTMLField
from cms.models.fields import PlaceholderField

from aldryn_translation_tools.models import TranslationHelperMixin
from aldryn_common.admin_fields.sortedm2m import SortedM2MModelField
from allink_core.core.models.models import AllinkBaseAppContentPlugin, AllinkBaseModel, AllinkBaseTranslatedFieldsModel
from allink_core.core.models.mixins import AllinkTranslatedAutoSlugifyMixin
from allink_core.core.loading import get_model, get_class


AllinkNewsManager = get_class('news.managers', 'AllinkNewsManager')


# News
class BaseNews(TranslationHelperMixin, AllinkTranslatedAutoSlugifyMixin, TranslatableModel, TimeFramedModel, AllinkBaseModel):
    slug_source_field_name = 'title'

    title = TranslatedField(any_language=True)
    slug = TranslatedField(any_language=True)
    lead = TranslatedField()

    preview_image = FilerImageField(
        verbose_name=_(u'Preview Image'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_preview_image',
    )
    template = models.CharField(
        _(u'Template'),
        help_text=_(u'Choose a template.'),
        max_length=50,
        blank=True,
        null=True,
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True
    )

    objects = AllinkNewsManager()

    header_placeholder = PlaceholderField(u'news_header', related_name='%(app_label)s_%(class)s_header_placeholder')
    content_placeholder = PlaceholderField(u'news_content', related_name='%(app_label)s_%(class)s_content_placeholder')
    content_additional_placeholder = PlaceholderField(u'news_content_additional', related_name='%(app_label)s_%(class)s_content_additional_placeholder')


    class Meta:
        abstract = True
        app_label = 'news'
        verbose_name = _('News entry')
        verbose_name_plural = _('News')


class BaseNewsTranslation(AllinkBaseTranslatedFieldsModel):
    master = models.ForeignKey('news.News', related_name='translations', null=True)

    title = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        _(u'Slug'),
        max_length=255,
        default='',
        blank=True,
        help_text=_(u'Leave blank to auto-generate a unique slug.')
    )
    lead = HTMLField(
        _(u'Lead Text'),
        help_text=_(u'Teaser text that in some cases is used in the list view and/or in the detail view.'),
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
        help_text=_('Select and arrange specific entries, or, leave blank to select all. (If '
                    'manual entries are selected the category filtering will be ignored.)')
    )

    def save(self, *args, **kwargs):
        # invalidate cache
        cache.delete_many([make_template_fragment_key('news_preview_image', [self.id, news.id]) for news in
                           get_model('news', 'News').objects.all()])
        super(BaseNewsAppContentPlugin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'news'
