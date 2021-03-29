# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from adminsortable.admin import SortableAdmin
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from parler.admin import TranslatableAdmin
from allink_core.core.admin import (
    AllinkMediaAdminMixin,
    AllinkSEOAdminMixin,
    AllinkCategoryAdminMixin,
    AllinkTeaserAdminMixin,
)

from .models import DummyApp


@admin.register(DummyApp)
class DummyAppAdmin(AllinkMediaAdminMixin, AllinkSEOAdminMixin, AllinkCategoryAdminMixin,
                    AllinkTeaserAdminMixin, PlaceholderAdminMixin, TranslatableAdmin, SortableAdmin):
    list_display = ('title', 'status', 'all_categories_column',)
    list_filter = ('status', 'categories',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'status',
                    'title',
                    'slug',
                    'lead',
                    'preview_image',
                )
            }),
        )

        fieldsets += self.get_category_fieldsets()
        fieldsets += self.get_teaser_fieldsets()
        fieldsets += self.get_seo_fieldsets()
        return fieldsets

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'lead':
            kwargs['widget'] = forms.Textarea
        return super(DummyAppAdmin, self).formfield_for_dbfield(db_field, **kwargs)
