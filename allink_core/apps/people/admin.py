# -*- coding: utf-8 -*-
from django.contrib import admin
from adminsortable.admin import SortableAdmin

from allink_core.core.loading import get_model
from parler.admin import TranslatableAdmin
from allink_core.core.admin import AllinkMediaAdminMixin, AllinkSEOAdminMixin, \
    AllinkCategoryAdminMixin, AllinkTeaserAdminMixin

People = get_model('people', 'People')


@admin.register(People)
class PeopleAdmin(AllinkMediaAdminMixin, AllinkSEOAdminMixin, AllinkCategoryAdminMixin, AllinkTeaserAdminMixin,
                  TranslatableAdmin, SortableAdmin):
    search_fields = ('first_name', 'last_name',)
    list_display = ('first_name', 'last_name', 'status', 'all_categories_column', 'created', 'modified',)
    view_on_site = False

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'status',
                    ('first_name', 'last_name'),
                    'job_function',
                    'preview_image',
                    ('email', 'website'),
                    'company_name',
                    ('phone', 'mobile', 'fax'),
                    ('street', 'street_nr'),
                    'street_additional',
                    ('place', 'zip_code'),
                    'country',
                    'slug',
                )
            }),
        )
        fieldsets += self.get_category_fieldsets()
        fieldsets += self.get_teaser_fieldsets()
        fieldsets += self.get_seo_fieldsets()
        return fieldsets
