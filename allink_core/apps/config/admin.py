# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _

from cms.extensions import PageExtensionAdmin

from solo.admin import SingletonModelAdmin
from webpack_loader.utils import get_files
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from allink_core.core.loading import get_model
from allink_core.core.forms.fields import ColorField
from allink_core.core.utils import get_project_color_choices

Config = get_model('config', 'Config')
AllinkPageExtension = get_model('config', 'AllinkPageExtension')
require_POST = method_decorator(require_POST)


class ConfigAdminForm(TranslatableModelForm):
    theme_color = ColorField(label=_(u'Theme Color'), help_text=_(u'Theme color for Android Chrome'), required=False)
    mask_icon_color = ColorField(label=_(u'Mask Icon Color'), help_text=_(u'Mask icon color for safari-pinned-tab.svg'), required=False)
    msapplication_tilecolor = ColorField(label=_(u'MS Application Title Color'), help_text=_(u'MS application TitleColor Field'), required=False)

    class Meta(forms.ModelForm):
        model = Config
        fields = ['theme_color', 'mask_icon_color', 'msapplication_tilecolor']


@admin.register(Config)
class ConfigAdmin(TranslatableAdmin, SingletonModelAdmin):
    form = ConfigAdminForm

    class Media:
        js = (
            get_files('djangocms_custom_admin')[0]['publicPath'],
        )
        css = {
            'all': (
                get_files('djangocms_custom_admin')[1]['publicPath'],

            )
        }

    def get_fieldsets(self, request, obj=None):

        if get_project_color_choices():
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
                    'google_site_verification',
                )
            }),
        else:
            fieldsets = (_('Site Meta'), {
                'classes': (
                    'collapse',
                ),
                'fields': (
                    'default_og_image',
                    'default_base_title',
                    'google_site_verification',
                )
            }),

        fieldsets += (_('Email'), {
            'classes': (
                'collapse',
            ),
            'fields': (
                'default_to_email',
                'default_from_email',
            )
        }),

        fieldsets += (_('App Names and Toolbar'), {
            'classes': (
                'collapse',
            ),
            'description': _(u'Please notice that the plugin names will only change after restarting the server.(Please redeploy with Divio Cloud Dashboard.)'),
            'fields': (
                ('news_verbose', 'news_verbose_plural', 'news_toolbar_enabled', ),
                ('events_verbose', 'events_verbose_plural', 'events_toolbar_enabled', ),
                ('locations_verbose', 'locations_verbose_plural', 'locations_toolbar_enabled', ),
                ('people_verbose', 'people_verbose_plural', 'people_toolbar_enabled', ),
                ('testimonials_verbose', 'testimonials_verbose_plural', 'testimonials_toolbar_enabled', ),
                ('work_verbose', 'work_verbose_plural', 'work_toolbar_enabled', ),
                ('members_verbose', 'members_verbose_plural', 'members_toolbar_enabled', ),
                ('contactrequest_verbose', 'contactrequest_verbose_plural', 'contactrequest_toolbar_enabled', ),
                ('eventsregistration_verbose', 'eventsregistration_verbose_plural', 'eventsregistration_toolbar_enabled', ),
                ('terms_verbose', 'terms_verbose_plural', 'terms_toolbar_enabled', ),
                'config_allink_page_toolbar_enabled',
            )
        }),

        fieldsets += (_('Gallery Plugin'), {
            'classes': (
                'collapse',
            ),
            'fields': (
                'gallery_plugin_caption_text_max_length',
            )
        }),

        return fieldsets


@admin.register(AllinkPageExtension)
class AllinkSEOExtensionAdmin(PageExtensionAdmin):
    pass

