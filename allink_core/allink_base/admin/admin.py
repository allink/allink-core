# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from adminsortable.admin import NonSortableParentAdmin
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
                    'title_size',
                    'slug',
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

