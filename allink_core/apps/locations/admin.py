# -*- coding: utf-8 -*-
from django.contrib import admin, messages
from adminsortable.admin import SortableAdmin
from allink_core.core.loading import get_model
from parler.admin import TranslatableAdmin
from allink_core.core.admin import AllinkMediaAdminMixin, AllinkSEOAdminMixin, \
    AllinkCategoryAdminMixin, AllinkTeaserAdminMixin

Locations = get_model('locations', 'Locations')


@admin.register(Locations)
class LocationsAdmin(AllinkMediaAdminMixin, AllinkSEOAdminMixin, AllinkCategoryAdminMixin, AllinkTeaserAdminMixin,
                     TranslatableAdmin, SortableAdmin):
    exclude = ('lead',)
    readonly_fields = ('is_currently_open',)
    list_display = ('title', 'status', 'all_categories_column',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'status',
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
                    'commercial_register_entry',
                    'preview_image',
                    'opening_hours_display',
                )
            }),
            ('Opening hours (Detailed)', {
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
                    'sun_afternoon'
                ),
                'description': 'Format: "9:00-12:00  13:00-20:00"'
            }),
        )
        fieldsets += self.get_category_fieldsets()
        fieldsets += self.get_teaser_fieldsets()
        fieldsets += self.get_seo_fieldsets()
        return fieldsets

    def save_model(self, request, obj, form, change):
        if obj.value_has_changed_for_fields(["place", "zip_code", "street", "street_additional"]) \
                and obj.place and obj.zip_code and obj.street:
            msg = obj.geocode_location()
            if not msg:
                messages.warning(request, msg)
        obj.save()
