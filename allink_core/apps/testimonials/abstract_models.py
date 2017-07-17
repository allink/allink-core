# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from cms.models.fields import PlaceholderField
from adminsortable.models import SortableMixin
from parler.models import TranslatableModel, TranslatedField, TranslatedFieldsModel
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

from aldryn_translation_tools.models import TranslationHelperMixin
from aldryn_common.admin_fields.sortedm2m import SortedM2MModelField
from allink_core.core.models.models import AllinkBaseAppContentPlugin, AllinkBaseModel, AllinkBaseTranslatedFieldsModel
from allink_core.core.models.mixins import AllinkTranslatedAutoSlugifyMixin
from allink_core.apps.testimonials.managers import AllinkTestimonialManager
from allink_core.core.loading import get_model


class BaseTestimonials(SortableMixin, TranslationHelperMixin, AllinkTranslatedAutoSlugifyMixin, TranslatableModel, AllinkBaseModel):

    slug_source_field_name = 'full_name'

    first_name = models.CharField(
        _(u'First Name'),
        max_length=255,
        default=''
    )
    last_name = models.CharField(
        _(u'Last Name'),
        max_length=255,
        default=''
    )

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

    header_placeholder = PlaceholderField(u'testimonials_header', related_name='%(app_label)s_%(class)s_header_placeholder')
    content_placeholder = PlaceholderField(u'testimonials_content', related_name='%(app_label)s_%(class)s_content_placeholder')

    objects = AllinkTestimonialManager()

    class Meta:
        abstract = True
        app_label = 'testimonials'
        ordering = ('sort_order',)
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')

    @property
    def full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @property
    def title(self):
        return u'{} {}'.format(self.first_name, self.last_name)


class BaseTestimonialsTranslation(AllinkBaseTranslatedFieldsModel):
    master = models.ForeignKey('testimonials.Testimonials', related_name='translations', null=True)

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
        app_label = 'testimonials'


class BaseTestimonialsAppContentPlugin(AllinkBaseAppContentPlugin):

    manual_entries = SortedM2MModelField(
        'testimonials.Testimonials',
        blank=True,
        help_text=_('Select and arrange specific entries, or, leave blank to select all. (If '
                    'manual entries are selected the category filtering will be ignored.)')
    )

    def save(self, *args, **kwargs):
        # invalidate cache
        cache.delete_many([make_template_fragment_key('testimonials_preview_image', [self.id, testimonials.id]) for testimonials in
                           get_model('testimonials', 'Testimonials').objects.all()])
        super(BaseTestimonialsAppContentPlugin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'testimonials'
