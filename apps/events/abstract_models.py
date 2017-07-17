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
from allink_core.core.models.models import AllinkBaseAppContentPlugin, AllinkBaseModel, AllinkSimpleRegistrationFieldsModel, AllinkBaseTranslatedFieldsModel
from allink_core.core.models.mixins import AllinkTranslatedAutoSlugifyMixin
from allink_core.core.loading import get_model, get_class


AllinkEventsManager = get_class('events.managers', 'AllinkEventsManager')



# Events
class BaseEvents(TranslationHelperMixin, AllinkTranslatedAutoSlugifyMixin, TranslatableModel, TimeFramedModel, AllinkBaseModel):
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

    header_placeholder = PlaceholderField(u'events_header', related_name='%(app_label)s_%(class)s_header_placeholder')
    content_placeholder = PlaceholderField(u'events_content', related_name='%(app_label)s_%(class)s_content_placeholder')
    content_additional_placeholder = PlaceholderField(u'events_content_additional', related_name='%(app_label)s_%(class)s_content_additional_placeholder')

    costs = TranslatedField()

    form_enabled = models.BooleanField(
        _(u'Event Form enabled'),
        default=True
    )

    event_date_time = models.DateTimeField(
        _(u'Event Date/ Time'),
        blank=True,
        null=True,
    )

    location = models.ForeignKey(
        'locations.Locations',
        blank=True,
        null=True,
        related_name='events'
    )

    objects = AllinkEventsManager()

    class Meta:
        abstract = True
        app_label = 'events'
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    def __str__(self):
        return u'%s %s' % (self.title, self.event_date_time)

    def show_registration_form(self):
        if getattr(self, 'event_date_time'):
            if self.event_date_time < datetime.now().date():
                return False
        if self.form_enabled:
            return True
        else:
            return False


class BaseEventsTranslation(AllinkBaseTranslatedFieldsModel):
    master = models.ForeignKey('events.Events', related_name='translations', null=True)

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
    costs = models.CharField(
        max_length=255,
        help_text=_(u'Costs'),
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
        app_label = 'events'


class BaseEventsAppContentPlugin(AllinkBaseAppContentPlugin):
    manual_entries = SortedM2MModelField(
        'events.Events',
        blank=True,
        help_text=_('Select and arrange specific entries, or, leave blank to select all. (If '
                    'manual entries are selected the category filtering will be ignored.)')
    )

    def save(self, *args, **kwargs):
        # invalidate cache
        cache.delete_many([make_template_fragment_key('events_preview_image', [self.id, event.id]) for event in
                           get_model('events', 'Events').objects.all()])
        super(BaseEventsAppContentPlugin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'events'


class BaseEventsRegistration(AllinkSimpleRegistrationFieldsModel):

    event = models.ForeignKey('events.Events', null=True)

    # terms = models.ForeignKey(
    #     'allink_terms.AllinkTerms',
    #     verbose_name=_(u'I have read and accept the terms and conditions.'),
    #     blank=True,
    #     null=True
    # )

    class Meta:
        abstract = True
        app_label = 'events'

    def __str__(self):
        return u'%s %s' % (self.first_name, self.last_name)

    @classmethod
    def get_verbose_name(cls):
        Config = get_model('config', 'Config')
        try:
            field_name = cls._meta.model_name + '_verbose'
            return getattr(Config.get_solo(), field_name)
        except:
            return cls._meta.verbose_name

    @classmethod
    def get_verbose_name_plural(cls):
        Config = get_model('config', 'Config')
        try:
            field_name = cls._meta.model_name + '_verbose_plural'
            return getattr(Config.get_solo(), field_name)
        except:
            return cls._meta.verbose_name_plural
