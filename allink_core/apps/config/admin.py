# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _

from cms.extensions import PageExtensionAdmin, TitleExtensionAdmin

from solo.admin import SingletonModelAdmin
from webpack_loader.utils import get_files
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from allink_core.core.loading import get_model
from allink_core.core.forms.fields import ColorField
from allink_core.core.utils import get_project_color_choices

Config = get_model('config', 'Config')
AllinkPageExtension = get_model('config', 'AllinkPageExtension')
AllinkTitleExtension = get_model('config', 'AllinkTitleExtension')
require_POST = method_decorator(require_POST)


class ConfigAdminForm(TranslatableModelForm):
    theme_color = ColorField(label=_(u'Theme Color'), help_text=_(u'Theme color for Android Chrome'), required=False)
    mask_icon_color = ColorField(label=_(u'Mask Icon Color'), help_text=_(u'Mask icon color for safari-pinned-tab.svg'), required=False)
    msapplication_tilecolor = ColorField(label=_(u'MS Application Title Color'), help_text=_(u'MS application TitleColor Field'), required=False)

    class Meta(forms.ModelForm):
        model = Config
        exclude = ()


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

        fieldsets += (_('Toolbar'), {
            'classes': (
                'collapse',
            ),
            'fields': (
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
class AllinkPageExtensionAdmin(PageExtensionAdmin):
    pass

@admin.register(AllinkTitleExtension)
class AllinkPageExtensionAdmin(TitleExtensionAdmin):
    pass

