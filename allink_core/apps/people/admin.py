# -*- coding: utf-8 -*-
from django.contrib import admin

from allink_core.core.loading import get_model
from allink_core.core.admin import AllinkBaseAdminSortable

People = get_model('people', 'People')


@admin.register(People)
class PeopleAdmin(AllinkBaseAdminSortable):
    search_fields = ('first_name', 'last_name',)
    list_display = ('first_name', 'last_name', 'get_categories', 'is_active', 'created', 'modified',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'is_active',
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
                ),
            }),
        )

        fieldsets += self.get_base_fieldsets()

        return fieldsets
