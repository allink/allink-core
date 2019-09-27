# -*- coding: utf-8 -*-

from django.contrib import admin
from parler.admin import TranslatableAdmin
from webpack_loader.utils import get_files

from allink_core.core.admin.forms import AllinkCategoryAdminForm
from allink_core.core.admin.mixins import AllinkSEOAdminMixin, AllinkCategoryAdminMixin, AllinkMediaAdminMixin


class AllinkBaseAdmin(AllinkMediaAdminMixin, AllinkSEOAdminMixin, TranslatableAdmin):
    """
    Base ModelAdmin used in combination with AllinkBaseTranslatableModel
    """
    search_fields = ('translations__title',)
    list_display = ('title', 'status', 'created', 'modified', 'all_languages_column',)
    list_filter = ('status',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets()
        fieldsets += (
            (None, {
                'fields': (
                    'status',
                    'title',
                    'lead',
                    'preview_image',
                    'slug',
                    'created',
                ),
            }),
        )
        fieldsets += self.get_seo_fieldsets()
        return fieldsets


class AllinkCategoryAdmin(AllinkCategoryAdminMixin, AllinkBaseAdmin):
    """
    ModelAdmin used in combination with AllinkCategoryModel
    """
    list_display = ('title', 'status', 'all_categories_column', 'created', 'modified', 'all_languages_column',)
    list_filter = (
        'status',
        ('categories', admin.RelatedOnlyFieldListFilter,),
    )

    form = AllinkCategoryAdminForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'status',
                    'title',
                    'lead',
                    'preview_image',
                    'slug',
                    'created',
                )
            }),
        )
        fieldsets += self.get_seo_fieldsets()
        fieldsets += self.get_category_fieldsets()
        return fieldsets

    def all_categories_column(self, object):
        return "\n|\n".join([c.name for c in object.categories.all()])

    all_categories_column.short_description = 'Categories'
