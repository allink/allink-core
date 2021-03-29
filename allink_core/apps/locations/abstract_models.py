# -*- coding: utf-8 -*-
import datetime
from functools import reduce
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from cms.models.fields import PageField
from cms.models.fields import PlaceholderField
from adminsortable.models import SortableMixin
from parler.models import TranslatedField
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

from allink_core.core.models.fields import SortedM2MModelField
from allink_core.core.loading import get_class
from allink_core.core.models import (
    AllinkCategoryFieldsModel,
    AllinkBaseTranslatableModel,
    AllinkBaseAppContentPlugin,
    AllinkContactFieldsModel,
    AllinkBaseTranslatedFieldsModel,
)

AllinkLocationsManager = get_class('locations.managers', 'AllinkLocationsManager')


class BaseLocations(SortableMixin, AllinkContactFieldsModel,
                    AllinkCategoryFieldsModel, AllinkBaseTranslatableModel):
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
            {'model': 'self', 'field': 'opening_hours_display', },
        ],
        'teaser_description': [
            {'model': 'self', 'field': 'teaser_description', },
            {'model': 'self', 'field': 'lead', },
        ],
        'teaser_link_text': [
            {'model': 'self', 'field': 'teaser_link_text', },
            {'model': 'self', 'field': 'TEASER_LINK_TEXT', },
        ],
    }
    slug_source_field_name = 'title'

    title = TranslatedField(any_language=True)
    subtitle = TranslatedField()
    lead = TranslatedField()
    country = TranslatedField()
    opening_hours_display = TranslatedField()
    preview_image = FilerImageField(
        verbose_name='Preview Image',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_preview_image',
    )
    lat = models.FloatField(
        'Latitude',
        blank=True,
        null=True
    )
    lng = models.FloatField(
        'Longitude',
        blank=True,
        null=True
    )
    map_link = models.URLField(
        'Map Link',
        help_text='This could be a <strong>Google Places</strong> or <strong>Directions</strong> link.',
        blank=True,
        null=True
    )
    commercial_register_entry = models.CharField(
        'Commercial register entry',
        blank=True,
        null=True,
        max_length=50,
    )
    mon = models.CharField(
        'Monday morning or whole day',
        help_text='Format: "(h)h:mm-(h)h:mm"', blank=True, max_length=100)
    tue = models.CharField(
        'Tuesday morning or whole day',
        help_text='Format: "(h)h:mm-(h)h:mm"', blank=True, max_length=100)
    wed = models.CharField(
        'Wednesday morning or whole day',
        help_text='Format: "(h)h:mm-(h)h:mm"', blank=True, max_length=100)
    thu = models.CharField(
        'Thursday morning or whole day',
        help_text='Format: "(h)h:mm-(h)h:mm"', blank=True, max_length=100)
    fri = models.CharField(
        'Friday morning or whole day',
        help_text='Format: "(h)h:mm-(h)h:mm"', blank=True, max_length=100)
    sat = models.CharField(
        'Saturday morning or whole day',
        help_text='Format: "(h)h:mm-(h)h:mm"', blank=True, max_length=100)
    sun = models.CharField(
        'Sunday morning or whole day',
        help_text='Format: "(h)h:mm-(h)h:mm"', blank=True, max_length=100)
    mon_afternoon = models.CharField(
        'Monday afternoon',
        help_text='Format: "(h)h:mm-(h)h:mm", only fill if location has a lunch break',
        blank=True, max_length=100
    )
    tue_afternoon = models.CharField(
        'Tuesday afternoon',
        help_text='Format: "(h)h:mm-(h)h:mm", only fill if location has a lunch break',
        blank=True, max_length=100
    )
    wed_afternoon = models.CharField(
        'Wednesday afternoon',
        help_text='Format: "(h)h:mm-(h)h:mm", only fill if location has a lunch break',
        blank=True, max_length=100
    )
    thu_afternoon = models.CharField(
        'Thursday afternoon',
        help_text='Format: "(h)h:mm-(h)h:mm", only fill if location has a lunch break',
        blank=True, max_length=100
    )
    fri_afternoon = models.CharField(
        'Friday afternoon',
        help_text='Format: "(h)h:mm-(h)h:mm", only fill if location has a lunch break',
        blank=True, max_length=100
    )
    sat_afternoon = models.CharField(
        'Saturday afternoon',
        help_text='Format: "(h)h:mm-(h)h:mm", only fill if location has a lunch break',
        blank=True, max_length=100
    )
    sun_afternoon = models.CharField(
        'Sunday afternoon',
        help_text='Format: "(h)h:mm-(h)h:mm", only fill if location has a lunch break',
        blank=True, max_length=100
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True
    )
    header_placeholder = PlaceholderField(
        'locations_header',
        related_name='%(app_label)s_%(class)s_header_placeholder'
    )
    content_placeholder = PlaceholderField(
        'locations_content',
        related_name='%(app_label)s_%(class)s_content_placeholder'
    )
    street = models.CharField(
        _('Street'),
        max_length=255,
        blank=True,
        null=True
    )
    street_nr = models.CharField(
        _('Street Nr.'),
        max_length=50,
        blank=True,
        null=True
    )
    street_additional = models.CharField(
        _('Address Additional'),
        max_length=255,
        blank=True,
        null=True
    )
    zip_code = models.CharField(
        _('Zip Code'),
        max_length=10,
        blank=True,
        null=True
    )
    place = models.CharField(
        _('Place'),
        max_length=255,
        blank=True,
        null=True
    )

    objects = AllinkLocationsManager()

    class Meta:
        abstract = True
        app_label = 'locations'
        ordering = 'sort_order',
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return '%s - %s' % (self.title, self.created.strftime('%d.%m.%Y'))

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
            street_full = '{} {}'.format(self.street, self.street_nr) + self.street_additional
            place, (lat, lng) = g.geocode('%s, %s %s, %s' % (street_full, self.zip_code, self.place, self.country))
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
    is_currently_open.short_description = 'Now open'

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
        except (KeyError, IndexError):
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
    def opening_hours(self):
        """
        Return the opening hours for whole days in a summarized format

        Monday – Friday	09:00-19:00
        Saturday	09:00-17:00
        """

        opening_times = [
            (_('Monday'), self.mon, self.mon_afternoon),
            (_('Tuesday'), self.tue, self.tue_afternoon),
            (_('Wednesday'), self.wed, self.wed_afternoon),
            (_('Thursday'), self.thu, self.thu_afternoon),
            (_('Friday'), self.fri, self.fri_afternoon),
            (_('Saturday'), self.sat, self.sat_afternoon),
            (_('Sunday'), self.sun, self.sun_afternoon)
        ]

        opening_hours = []
        for i, opening_time in enumerate(opening_times):
            day, morning, afternoon = opening_time
            morning = morning.replace('-', ' – ')
            afternoon = afternoon.replace('-', ' – ')

            if not morning and not afternoon:
                day = {}
                opening_hours.append(day)
            elif len(opening_hours) \
                      and morning == list(map(lambda x: x.get('morning'), opening_hours))[-1] \
                    and afternoon == list(map(lambda x: x.get('afternoon'), opening_hours))[-1]:
                opening_hours[-1]['end_day'] = day
            else:
                day = {
                    'start_day': day,
                    'end_day': day,
                    'morning': morning,
                    'afternoon': afternoon,
                }
                opening_hours.append(day)

        return opening_hours

    @cached_property
    def gmaps_link(self):
        """
        Returns google maps link with query of current store
        """
        return ("https://www.google.ch/maps?q=%(name)s+%(street)s+%(zip_code)s+%(place)s" % {
            'name': self.title,
            'street': '{} {} {}'.format(self.street, self.street_nr, self.street_additional),
            'zip_code': self.zip_code,
            'place': self.place
        }).replace(' ', '+')


class BaseLocationsTranslation(AllinkBaseTranslatedFieldsModel):
    master = models.ForeignKey(
        'locations.Locations',
        on_delete=models.CASCADE,
        related_name='translations',
        null=True
    )
    title = models.CharField(
        max_length=255
    )
    subtitle = models.CharField(
        'Subtitle',
        max_length=255,
        blank=True,
        null=True,
    )
    lead = HTMLField(
        'Lead Text',
        help_text='Teaser text that in some cases is used in the list view and/or in the detail view.',
        blank=True,
        null=True,
    )
    opening_hours_display = HTMLField(
        'Opening hours',
        help_text=('This Text will be used to show the Opening hours on the location detail page. '
                   'If provided, the detailed opening hours will be overriden.'),
        blank=True,
        null=True,
    )
    country = models.CharField(
        _('Country'),
        max_length=255,
        blank=True,
        null=True
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
        help_text='Select and arrange specific entries, or, leave blank to select all. (If '
                  'manual entries are selected the category filtering will be applied as well.)'
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
        related_name="load_more_internallink_locations",
        blank=True,
        null=True,
    )
    zoom_level = models.IntegerField(
        'Zoom Level',
        help_text='The higher the number, the more we zoom in.',
        choices=ZOOM_LEVEL_CHOICES,
        default=14
    )

    def save(self, *args, **kwargs):
        super(BaseLocationsAppContentPlugin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'locations'
