# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from parler.admin import TranslatableAdmin
from allink_core.core.admin import AllinkMediaAdminMixin, AllinkSEOAdminMixin, AllinkCategoryAdminMixin, \
    AllinkTeaserAdminMixin, AllinkCategoryAdminForm
from allink_core.core.loading import get_model
from allink_core.core.utils import get_additional_choices

News = get_model('news', 'News')


class NewsContentAdminForm(AllinkCategoryAdminForm):

    def __init__(self, *args, **kwargs):
        super(NewsContentAdminForm, self).__init__(*args, **kwargs)

        if get_additional_choices('ADDITIONAL_NEWS_DETAIL_TEMPLATES'):
            self.fields['template'] = forms.CharField(
                label='Template',
                widget=forms.Select(choices=get_additional_choices('ADDITIONAL_NEWS_DETAIL_TEMPLATES', blank=True)),
                required=False,
            )
        else:
            self.fields['template'] = forms.CharField(widget=forms.HiddenInput(), required=False)


@admin.register(News)
class NewsAdmin(AllinkMediaAdminMixin, AllinkSEOAdminMixin, AllinkCategoryAdminMixin,
                AllinkTeaserAdminMixin, PlaceholderAdminMixin,
                TranslatableAdmin):
    form = NewsContentAdminForm
    list_display = ('title', 'status', 'all_categories_column','entry_date',)

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

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'lead':
            kwargs['widget'] = forms.Textarea
            kwargs['max_length'] = 400
            kwargs['help_text'] = 'Max. 400 characters.'
        return super(NewsAdmin, self).formfield_for_dbfield(db_field, **kwargs)
