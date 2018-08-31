# -*- coding: utf-8 -*-
import datetime
from functools import reduce
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils.functional import cached_property

from cms.models.fields import PageField
from cms.models.fields import PlaceholderField
from adminsortable.models import SortableMixin
from parler.models import TranslatableModel, TranslatedField
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

from aldryn_translation_tools.models import TranslationHelperMixin
from aldryn_common.admin_fields.sortedm2m import SortedM2MModelField
from allink_core.core.models.models import AllinkBaseAppContentPlugin, AllinkBaseModel, AllinkContactFieldsModel, AllinkAddressFieldsModel, AllinkBaseTranslatedFieldsModel
from allink_core.core.models.mixins import AllinkTranslatedAutoSlugifyMixin
from allink_core.core.models.managers import AllinkBaseModelManager


class BaseLocations(SortableMixin, TranslationHelperMixin, AllinkTranslatedAutoSlugifyMixin, TranslatableModel, AllinkContactFieldsModel, AllinkAddressFieldsModel, AllinkBaseModel):
    slug_source_field_name = 'title'

    title = TranslatedField(any_language=True)
    slug = TranslatedField(any_language=True)
    subtitle = TranslatedField()
    lead = TranslatedField()
    opening_hours_display = TranslatedField()

    preview_image = FilerImageField(
        verbose_name=_(u'Preview Image'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_preview_image',
    )

    lat = models.FloatField(
        _(u'Latitude'),
        blank=True,
        null=True
    )
    lng = models.FloatField(
        _(u'Longitude'),
        blank=True,
        null=True
    )

    map_link = models.URLField(
        _(u'Map Link'),
        help_text=_(u'This could be a <strong>Google Places</strong> or <strong>Directions</strong> link.'),
        blank=True,
        null=True
    )

    mon = models.CharField(_(u'Monday morning or whole day'), help_text=u'Format: "(h)h:mm-(h)h:mm"', blank=True, max_length=100)
    tue = models.CharField(_(u'Tuesday morning or whole day'), help_text=u'Format: "(h)h:mm-(h)h:mm"', blank=True, max_length=100)
    wed = models.CharField(_(u'Wednesday morning or whole day'), help_text=u'Format: "(h)h:mm-(h)h:mm"', blank=True, max_length=100)
    thu = models.CharField(_(u'Thursday morning or whole day'), help_text=u'Format: "(h)h:mm-(h)h:mm"', blank=True, max_length=100)
    fri = models.CharField(_(u'Friday morning or whole day'), help_text=u'Format: "(h)h:mm-(h)h:mm"', blank=True, max_length=100)
    sat = models.CharField(_(u'Saturday morning or whole day'), help_text=u'Format: "(h)h:mm-(h)h:mm"', blank=True, max_length=100)
    sun = models.CharField(_(u'Sunday morning or whole day'), help_text=u'Format: "(h)h:mm-(h)h:mm"', blank=True, max_length=100)
    mon_afternoon = models.CharField(_(u'Monday afternoon'), help_text=u'Format: "(h)h:mm-(h)h:mm", only fill if location has a lunch break', blank=True, max_length=100)
    tue_afternoon = models.CharField(_(u'Tuesday afternoon'), help_text=u'Format: "(h)h:mm-(h)h:mm", only fill if location has a lunch break', blank=True, max_length=100)
    wed_afternoon = models.CharField(_(u'Wednesday afternoon'), help_text=u'Format: "(h)h:mm-(h)h:mm", only fill if location has a lunch break', blank=True, max_length=100)
    thu_afternoon = models.CharField(_(u'Thursday afternoon'), help_text=u'Format: "(h)h:mm-(h)h:mm", only fill if location has a lunch break', blank=True, max_length=100)
    fri_afternoon = models.CharField(_(u'Friday afternoon'), help_text=u'Format: "(h)h:mm-(h)h:mm", only fill if location has a lunch break', blank=True, max_length=100)
    sat_afternoon = models.CharField(_(u'Saturday afternoon'), help_text=u'Format: "(h)h:mm-(h)h:mm", only fill if location has a lunch break', blank=True, max_length=100)
    sun_afternoon = models.CharField(_(u'Sunday afternoon'), help_text=u'Format: "(h)h:mm-(h)h:mm", only fill if location has a lunch break', blank=True, max_length=100)

    sort_order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True
    )

    header_placeholder = PlaceholderField(u'locations_header', related_name='%(app_label)s_%(class)s_header_placeholder')
    content_placeholder = PlaceholderField(u'locations_content', related_name='%(app_label)s_%(class)s_content_placeholder')

    objects = AllinkBaseModelManager()

    class Meta:
        abstract = True
        app_label = 'locations'
        ordering = ('sort_order',)
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

    def value_has_changed_for_fields(instance, fields):
        """
        Did any field values change since the last time they were saved?
        """
        if not instance.pk:  # if new
            return True
        old_values = instance.__class__._default_manager.filter(pk=instance.pk).values().get()
        for f in fields:
            if not getattr(instance, f) == old_values[f]:
                return True
        return False

    def geocode_location(self):
        """
        Update lat and lng fields based on address
        """
        from geopy import geocoders
        g = geocoders.GoogleV3()
        try:
            street_full = u'{} {}'.format(self.street, self.street_nr) + self.street_additional
            place, (lat, lng) = g.geocode(u'%s, %s %s, %s' % (street_full, self.zip_code, self.place, self.country))
        except Exception as e:
            return "%s: %s" % (self, e)
        else:
            self.lat = lat
            self.lng = lng
        return True

    def is_currently_open(self):
        opening_times = [
            (self.mon, self.mon_afternoon),
            (self.tue, self.tue_afternoon),
            (self.wed, self.wed_afternoon),
            (self.thu, self.thu_afternoon),
            (self.fri, self.fri_afternoon),
            (self.sat, self.sat_afternoon),
            (self.sun, self.sun_afternoon)
        ]
        return self.opening_info(opening_times[datetime.date.today().weekday()])
    is_currently_open.boolean = True
    is_currently_open.short_description = _(u'Now open')

    def opening_info(self, times):
        """
        For the given times attr and the current time,
        is our store open?
        """
        morning = times[0]
        afternoon = times[1]

        try:
            current_time = datetime.datetime.today().time()
            morning_splited = morning.split('-')

            start_morning = morning_splited[0]
            end_morning = morning_splited[1]

            start_time = datetime.datetime.strptime(start_morning, '%H:%M').time()
            end_time = datetime.datetime.strptime(end_morning, '%H:%M').time()

            if start_time < current_time and end_time > current_time:
                return True

            elif afternoon:
                afternoon_splited = afternoon.split('-')

                start_afternoon = afternoon_splited[0]
                end_afternoon = afternoon_splited[1]

                start_time_afternoon = datetime.datetime.strptime(start_afternoon, '%H:%M').time()
                end_time_afternoon = datetime.datetime.strptime(end_afternoon, '%H:%M').time()

                if start_time_afternoon < current_time and end_time_afternoon > current_time:
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def has_opening_info(self):
        """
        Returns whether store has any filled in opening info
        If all fields are empty, returns False, else True
        """
        return reduce(
            lambda x, y: x or y,
            [
                self.mon,
                self.mon_afternoon,
                self.tue,
                self.tue_afternoon,
                self.wed,
                self.wed_afternoon,
                self.thu,
                self.thu_afternoon,
                self.fri,
                self.fri_afternoon,
                self.sat,
                self.sat_afternoon,
                self.sun,
                self.sun_afternoon
            ],
            False
        )

    @cached_property
    def gmaps_link(self):
        """
        Returns google maps link with query of current store
        """
        return (u"https://www.google.ch/maps?q=%(name)s+%(street)s+%(zip_code)s+%(place)s" % {
            'name': self.title,
            'street': u'{} {} {}'.format(self.street, self.street_nr, self.street_additional),
            'zip_code': self.zip_code,
            'place': self.place
        }).replace(' ', '+')


class BaseLocationsTranslation(AllinkBaseTranslatedFieldsModel):
    master = models.ForeignKey('locations.Locations', related_name='translations', null=True)

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
    subtitle = models.CharField(
        _(u'Subtitle'),
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
    opening_hours_display = HTMLField(
        _(u'Opening hours'),
        help_text=_(
            u'This Text will be used to show the Opening hours on the location detail page. If provided, the detailed opening hours will be overriden.'),
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
        app_label = 'locations'


class BaseLocationsAppContentPlugin(AllinkBaseAppContentPlugin):

    ZOOM_LEVEL_CHOICES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
        (13, 13),
        (14, 14),
        (15, 15),
        (16, 16),
        (17, 17),
        (18, 18),
    )

    manual_entries = SortedM2MModelField(
        'locations.Locations',
        blank=True,
        help_text=_('Select and arrange specific entries, or, leave blank to select all. (If '
                    'manual entries are selected the category filtering will be ignored.)')
    )
    apphook_page = PageField(
        verbose_name=_(u'Apphook Page'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_(u'If provided, this Apphook-Page will be used to generate the detail link.'),
    )

    zoom_level = models.IntegerField(
        _(u'Zoom Level'),
        help_text=_(u'The higher the number, the more we zoom in.'),
        choices=ZOOM_LEVEL_CHOICES,
        default=14
    )

    def save(self, *args, **kwargs):
        super(BaseLocationsAppContentPlugin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'locations'
