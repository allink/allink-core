# -*- coding: utf-8 -*-
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from adminsortable.admin import SortableAdmin, NonSortableParentAdmin, SortableStackedInline
from parler.admin import TranslatableAdmin
from aldryn_translation_tools.admin import AllTranslationsMixin

from .forms import AllinkBaseAdminForm



class AllinkBaseAdmin(NonSortableParentAdmin, AllTranslationsMixin, TranslatableAdmin):
    """
      Inlines for images have to be handled in the specific admin class

    """
    form = AllinkBaseAdminForm
    search_fields = ('title',)
    list_display = ('title', 'get_categories', 'active', 'created', 'modified')
    list_filter = ('active',)

    exclude = ('images',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'title',
                    'title_size',
                    'slug',
                    'active',
                ),
            }),
        )

        if self.model.get_can_have_categories():
            fieldsets += (_('Categories'), {
                # 'classes': ('collapse',),
                'fields': (
                    'categories',
                )
            }),

        return fieldsets

    def get_categories(self, object):
        return "\n|\n".join([c.name for c in object.categories.all()])

