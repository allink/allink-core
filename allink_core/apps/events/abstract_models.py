# -*- coding: utf-8 -*-
import datetime
from django.db import models

from cms.models.fields import PageField
from parler.models import TranslatedField
from filer.fields.image import FilerImageField
from djangocms_text_ckeditor.fields import HTMLField
from cms.models.fields import PlaceholderField

from aldryn_common.admin_fields.sortedm2m import SortedM2MModelField
from allink_core.core.models import (
    AllinkCategoryFieldsModel,
    AllinkBaseTranslatableModel,
    AllinkBaseTranslatedFieldsModel,
    AllinkBaseAppContentPlugin,
    AllinkSimpleRegistrationFieldsModel,
    AllinkTimeFramedModel,
)
from allink_core.core.loading import get_class

AllinkEventsManager = get_class('events.managers', 'AllinkEventsManager')


class BaseEvents(AllinkTimeFramedModel, AllinkCategoryFieldsModel, AllinkBaseTranslatableModel):
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
    template = models.CharField(
        'Template',
        help_text='Choose a template.',
        max_length=50,
        blank=True,
        null=True,
    )
    header_placeholder = PlaceholderField(
        'events_header',
        related_name='%(app_label)s_%(class)s_header_placeholder'
    )
    content_placeholder = PlaceholderField(
        'events_content',
        related_name='%(app_label)s_%(class)s_content_placeholder'
    )

    costs = TranslatedField()

    form_enabled = models.BooleanField(
        'Event Form enabled',
        default=True
    )
    entry_date = models.DateTimeField(
        'Entry Date',
    )
    location = models.ForeignKey(
        'locations.Locations',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='events'
    )

    objects = AllinkEventsManager()

    class Meta:
        abstract = True
        app_label = 'events'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return '%s %s' % (self.title, self.entry_date.strftime('%d.%m.%Y %H:%M:%S'))

    def show_registration_form(self):
        if getattr(self, 'entry_date'):
            if self.entry_date < datetime.now().date():
                return False
        if self.form_enabled:
            return True
        else:
            return False


class BaseEventsTranslation(AllinkBaseTranslatedFieldsModel):
    master = models.ForeignKey(
        'events.Events',
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
    costs = models.CharField(
        max_length=255,
        help_text='Costs',
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
        app_label = 'events'


class BaseEventsAppContentPlugin(AllinkBaseAppContentPlugin):
    # FILTERING
    DEFAULT = 'default'
    UPCOMING = 'upcoming'
    PAST = 'past'

    FILTERING = (
        (DEFAULT, '---------'),
        (UPCOMING, 'upcoming'),
        (PAST, 'past'),
    )

    manual_entries = SortedM2MModelField(
        'events.Events',
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

    class Meta:
        abstract = True
        app_label = 'events'

    def _apply_filtering_to_queryset_for_display(self, queryset):
        # upcoming
        if self.manual_filtering == BaseEventsAppContentPlugin.UPCOMING:
            return queryset.upcoming_entries()
        # past
        elif self.manual_filtering == BaseEventsAppContentPlugin.PAST:
            return queryset.past_entries()
        return queryset

    def save(self, *args, **kwargs):
        super(BaseEventsAppContentPlugin, self).save(*args, **kwargs)


class BaseEventsRegistration(AllinkSimpleRegistrationFieldsModel):
    event = models.ForeignKey(
        'events.Events',
        on_delete=models.CASCADE,
        null=True
    )

    # terms = models.ForeignKey(
    #     'allink_terms.AllinkTerms',
    #     verbose_name=('I have read and accept the terms and conditions.'),
    #     blank=True,
    #     null=True
    # )

    class Meta:
        abstract = True
        app_label = 'events'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
