# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from cms.models.fields import PlaceholderField
from adminsortable.models import SortableMixin
from parler.models import TranslatableModel, TranslatedField
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

from aldryn_translation_tools.models import TranslationHelperMixin
from aldryn_common.admin_fields.sortedm2m import SortedM2MModelField
from allink_core.core.models.models import AllinkBaseAppContentPlugin, AllinkBaseSearchPlugin, AllinkBaseModel, AllinkBaseTranslatedFieldsModel
from allink_core.core.models.mixins import AllinkTranslatedAutoSlugifyMixin
from allink_core.core.models.managers import AllinkBaseModelManager
from allink_core.core.loading import get_model


class BaseWork(SortableMixin, TranslationHelperMixin, AllinkTranslatedAutoSlugifyMixin, TranslatableModel, AllinkBaseModel):
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
    sort_order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True
    )

    header_placeholder = PlaceholderField(u'work_header', related_name='%(app_label)s_%(class)s_header_placeholder')
    content_placeholder = PlaceholderField(u'work_content', related_name='%(app_label)s_%(class)s_content_placeholder')
    content_additional_placeholder = PlaceholderField(u'work_content_additional', related_name='%(app_label)s_%(class)s_content_additional_placeholder')

    objects = AllinkBaseModelManager()

    class Meta:
        abstract = True
        app_label = 'work'
        ordering = ('sort_order',)
        verbose_name = _('Project / Reference')
        verbose_name_plural = _('Projects / References')


class BaseWorkTranslation(AllinkBaseTranslatedFieldsModel):
    master = models.ForeignKey('work.Work', related_name='translations', null=True)

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
        app_label = 'work'


class BaseWorkAppContentPlugin(AllinkBaseAppContentPlugin):

    manual_entries = SortedM2MModelField(
        'work.Work',
        blank=True,
        help_text=_('Select and arrange specific entries, or, leave blank to select all. (If '
                    'manual entries are selected the category filtering will be ignored.)')
    )

    def save(self, *args, **kwargs):
        # invalidate cache
        cache.delete_many([make_template_fragment_key('work_preview_image', [self.id, work.id]) for work in
                           get_model('work', 'Work').objects.all()])
        super(BaseWorkAppContentPlugin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'work'


class BaseWorkSearchPlugin(AllinkBaseSearchPlugin):

    class Meta:
        abstract = True
        app_label = 'work'

