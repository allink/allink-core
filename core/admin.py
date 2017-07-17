# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

from adminsortable.admin import NonSortableParentAdmin, SortableAdmin
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm
from aldryn_translation_tools.admin import AllTranslationsMixin
from webpack_loader.utils import get_files


class AllinkBaseAdminForm(TranslatableModelForm):

    def __init__(self, *args, **kwargs):
        super(AllinkBaseAdminForm, self).__init__(*args, **kwargs)
        # if app uses categories, populate 'categories' field
        if self.instance.__class__.get_can_have_categories():
            self.fields['categories'] = forms.ModelMultipleChoiceField(
                label=_(u'Categories'),
                widget=FilteredSelectMultiple(
                    verbose_name=_(u'Categories'),
                    is_stacked=True
                ),
                required=True,
                queryset=self.instance.get_relevant_categories()
            )
            self.fields['category_navigation'] = forms.ModelMultipleChoiceField(
                label=_(u'Categories for Navigation'),
                widget=FilteredSelectMultiple(
                    verbose_name=_(u'Categories for Navigation'),
                    is_stacked=True
                ),
                help_text=_(
                    u'You can explicitly define the categories for the category navigation here. This will override the automatically set of categories. (From "Filter & Ordering" but not from the "Manual entries")'),
                required=False,
                queryset=self.instance.get_relevant_categories()
            )


class AllinkBaseAdminBase(AllTranslationsMixin, TranslatableAdmin):
    """
      Inlines for images have to be handled in the specific admin class

    """
    form = AllinkBaseAdminForm
    search_fields = ('translations__title',)
    list_display = ('title', 'get_categories', 'is_active', 'created', 'modified')
    list_filter = (
        'is_active',
        ('categories', admin.RelatedOnlyFieldListFilter,),
    )

    exclude = ('images',)

    class Media:
        js = (get_files('djangocms_custom_admin')[0]['publicPath'], )
        css = {
            'all': (get_files('djangocms_custom_admin')[1]['publicPath'], )
        }

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'is_active',
                    'title',
                    'lead',
                    'preview_image',
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
                'fields': (
                    'categories',
                )
            }),
        else:
            fieldsets = ()

        fieldsets += (_('SEO'), {
            'classes': (
                'collapse',
            ),
            'fields': (
                'og_image',
                'og_title',
                'og_description',
                'disable_base_title',
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
