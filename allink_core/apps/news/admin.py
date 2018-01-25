# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from cms.admin.placeholderadmin import PlaceholderAdminMixin


from allink_core.core.admin import AllinkBaseAdminSortable
from allink_core.core.admin import AllinkBaseAdminForm
from allink_core.core_apps.allink_categories.models import AllinkCategory
from allink_core.core.loading import get_model
from allink_core.core.utils import get_additional_choices

News = get_model('news', 'News')


class NewsContentAdminForm(AllinkBaseAdminForm):

    def __init__(self, *args, **kwargs):
        super(NewsContentAdminForm, self).__init__(*args, **kwargs)

        if get_additional_choices('ADDITIONAL_NEWS_DETAIL_TEMPLATES'):
            self.fields['template'] = forms.CharField(
                label=_(u'Template'),
                widget=forms.Select(choices=get_additional_choices('ADDITIONAL_NEWS_DETAIL_TEMPLATES', blank=True)),
                required=False,
            )
        else:
            self.fields['template'] = forms.CharField(widget=forms.HiddenInput(), required=False)


@admin.register(News)
class NewsAdmin(PlaceholderAdminMixin, AllinkBaseAdminSortable):
    form = NewsContentAdminForm

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'lead':
            kwargs['widget'] = forms.Textarea
            kwargs['max_length'] = 400
            kwargs['help_text'] = _(u'Max. 400 characters.')
        return super(NewsAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'status',
                    'title',
                    'slug',
                    'created',
                    'template',
                    'preview_image',
                    'lead',
                ),
            }),
        )

        fieldsets += (_('Published From/To'), {
            'classes': ('collapse',),
            'fields': (
                'start',
                'end',
            )
        }),

        fieldsets += self.get_base_fieldsets()
        return fieldsets
