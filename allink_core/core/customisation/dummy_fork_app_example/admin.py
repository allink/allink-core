# -*- coding: utf-8 -*-
"""
use core:
from allink_core.apps.dummy_app.admin import *  # noqa
"""
from allink_core.apps.dummy_app.admin import *  # noqa

admin.site.unregister(DummyApp)


@admin.register(DummyApp)
class DummyAppAdmin(DummyAppAdmin):
    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'status',
                    'title',
                    'slug',
                    'entry_date',
                    'template',
                    'preview_image',
                    'lead',
                    'some_field',
                    'some_field_translated_field',

                )
            }),
        )

        fieldsets += (
            ('Published From/To', {
                'classes': ('collapse',),
                'fields': (
                    'start',
                    'end',
                )
            }),
        )

        fieldsets += self.get_category_fieldsets()
        fieldsets += self.get_teaser_fieldsets()
        fieldsets += self.get_seo_fieldsets()
        return fieldsets
