# -*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _

from allink_core.core.loading import get_model
from allink_core.core.admin import AllinkBaseAdminSortable

Locations = get_model('locations', 'Locations')


@admin.register(Locations)
class LocationsAdmin(AllinkBaseAdminSortable):
    exclude = ('lead', )
    readonly_fields = ('is_currently_open', )

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'is_active',
                    'title',
                    'slug',
                    'subtitle',
                    ('lat', 'lng',),
                    ('street', 'street_nr',),
                    'street_additional',
                    ('zip_code', 'place',),
                    'country',
                    ('phone', 'mobile',),
                    ('email', 'fax',),
                    'website',
                    'map_link',
                    'preview_image',
                    'opening_hours_display',
                ),
            }),
            (_(u'Opening hours (Detailed)'), {
                'classes': ('collapse',),
                'fields': (
                    'is_currently_open',
                    'mon',
                    'mon_afternoon',
                    'tue',
                    'tue_afternoon',
                    'wed',
                    'wed_afternoon',
                    'thu',
                    'thu_afternoon',
                    'fri',
                    'fri_afternoon',
                    'sat',
                    'sat_afternoon',
                    'sun',
                    'sun_afternoon'),
                    'description': _(u'Format: "9:00-12:00  13:00-20:00"'
                )
            }),
        )

        fieldsets += self.get_base_fieldsets()

        return fieldsets

    def save_model(self, request, obj, form, change):
        if obj.value_has_changed_for_fields(["place", "zip_code", "street", "street_additional"]) and obj.place and obj.zip_code and obj.street:
            msg = obj.geocode_location()
            if not msg:
                messages.warning(request, msg)
        obj.save()

