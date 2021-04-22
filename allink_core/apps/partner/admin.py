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

from allink_core.core.loading import get_model

Partner = get_model('partner', 'Partner')


@admin.register(Partner)
class PartnerAdmin(AllinkMediaAdminMixin, AllinkSEOAdminMixin, AllinkCategoryAdminMixin,
                   AllinkTeaserAdminMixin, PlaceholderAdminMixin, TranslatableAdmin, SortableAdmin):
    list_display = ('title', 'status', 'all_categories_column',)
    list_filter = ('status', 'categories',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'status',
                    'title',
                    'preview_image',
                    'link',
                    'internallink',
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
        return super(PartnerAdmin, self).formfield_for_dbfield(db_field, **kwargs)
