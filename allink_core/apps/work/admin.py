# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from cms.admin.placeholderadmin import PlaceholderAdminMixin
from adminsortable.admin import SortableAdmin
from parler.admin import TranslatableAdmin
from allink_core.core.loading import get_model
from allink_core.core.admin import AllinkMediaAdminMixin, AllinkSEOAdminMixin, \
    AllinkCategoryAdminMixin, AllinkTeaserAdminMixin

Work = get_model('work', 'Work')


@admin.register(Work)
class WorkAdmin(AllinkMediaAdminMixin, AllinkSEOAdminMixin, AllinkCategoryAdminMixin,
                AllinkTeaserAdminMixin, PlaceholderAdminMixin,
                TranslatableAdmin, SortableAdmin):
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
        fieldsets += self.get_seo_fieldsets()
        return fieldsets

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'lead':
            kwargs['widget'] = forms.Textarea
        return super(WorkAdmin, self).formfield_for_dbfield(db_field, **kwargs)
