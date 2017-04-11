# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _

from cms.extensions import TitleExtensionAdmin
from solo.admin import SingletonModelAdmin

from allink_core.allink_config.models import AllinkConfig, AllinkMetaTagExtension
from allink_core.allink_base.forms.fields import ColorField

require_POST = method_decorator(require_POST)


class AllinkConfigAdminForm(forms.ModelForm):
    theme_color = ColorField(label=_(u'Theme Color'), initial='#ffffff')

    class Meta(forms.ModelForm):
        model = AllinkConfig
        fields = ['theme_color']


@admin.register(AllinkConfig)
class AllinkConfigAdmin(SingletonModelAdmin):
    form = AllinkConfigAdminForm

    def get_fieldsets(self, request, obj=None):

        fieldsets = (_('Site Meta'), {
            'classes': (
                'collapse',
            ),
            'fields': (
                'default_og_image',
                'default_base_title',
                'theme_color',
                'mask_icon_color',
                'msapplication_tilecolor',
            )
        }),

        fieldsets += (_('App Names and Toolbar'), {
            'classes': (
                'collapse',
            ),
            'description': _(u'Please notice that the plugin names will only change after restarting the server.(Please redeploy with Divio Cloud Dashboard.)'),
            'fields': (
                ('blog_verbose', 'blog_verbose_plural', 'blog_toolbar_enabled', ),
                ('news_verbose', 'news_verbose_plural', 'news_toolbar_enabled', ),
                ('events_verbose', 'events_verbose_plural', 'events_toolbar_enabled', ),
                ('locations_verbose', 'locations_verbose_plural', 'locations_toolbar_enabled', ),
                ('people_verbose', 'people_verbose_plural', 'people_toolbar_enabled', ),
                ('testimonial_verbose', 'testimonial_verbose_plural', 'testimonial_toolbar_enabled', ),
                ('work_verbose', 'work_verbose_plural', 'work_toolbar_enabled', ),
                ('members_verbose', 'members_verbose_plural', 'members_toolbar_enabled', ),
                ('contact_verbose', 'contact_verbose_plural', 'contact_toolbar_enabled', ),
                ('events_registration_verbose', 'events_registration_verbose_plural', 'events_registration_toolbar_enabled', ),
            )
        }),

        return fieldsets

@admin.register(AllinkMetaTagExtension)
class AllinkMetaTagExtensionAdmin(TitleExtensionAdmin):
    pass
