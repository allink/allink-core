# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.core.cache import cache

from adminsortable.admin import NonSortableParentAdmin, SortableAdmin
from parler.admin import TranslatableAdmin
from aldryn_translation_tools.admin import AllTranslationsMixin

from .forms import AllinkBaseAdminForm


class AllinkBaseAdminBase(AllTranslationsMixin, TranslatableAdmin):
    """
      Inlines for images have to be handled in the specific admin class

    """
    form = AllinkBaseAdminForm
    search_fields = ('translations__title',)
    list_display = ('title', 'get_categories', 'active', 'created', 'modified')
    list_filter = (
        'active',
        ('categories', admin.RelatedOnlyFieldListFilter,),
    )

    exclude = ('images',)

    class Media:
        js = ('build/djangocms_custom_admin_scripts.js', )
        css = {
             'all': ('build/djangocms_custom_admin_style.css', )
        }

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'active',
                    'title',
                    'slug',
                    'created',
                ),
            }),
        )

        fieldsets += self.get_base_fieldsets()
        return fieldsets

    def get_base_fieldsets(self):
        if self.model.get_can_have_categories():
            fieldsets = (_('Categories'), {
                # 'classes': ('collapse',),
                'fields': (
                    'categories',
                )
            }),
        else:
            fieldsets = ()

        fieldsets += (_('Meta Tags'), {
                'classes': (
                    'collapse',
                ),
                'fields': (
                    'og_image',
                    'og_title',
                    'og_description',
                )
            }),

        return fieldsets

    def get_categories(self, object):
        return "\n|\n".join([c.name for c in object.categories.all()])

    get_categories.short_description = _(u'Categories')



class AllinkBaseAdmin(NonSortableParentAdmin, AllinkBaseAdminBase):
    pass


class AllinkBaseAdminSortable(SortableAdmin, AllinkBaseAdminBase):
    def do_sorting_view(self, request, model_type_id=None):
        super(AllinkBaseAdminSortable, self).do_sorting_view(request, model_type_id)
        cache.clear()
