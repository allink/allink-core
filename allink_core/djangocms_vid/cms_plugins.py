# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from webpack_loader.utils import get_files

from cms.plugin_pool import plugin_pool
from allink_core.djangocms_vid.models import AllinkVidEmbedPlugin, AllinkVidFilePlugin
from allink_core.djangocms_vid.forms import AllinkVidEmbedPluginForm, AllinkVidFilePluginForm


@plugin_pool.register_plugin
class CMSAllinkVidEmbedPlugin(CMSPluginBase):
    model = AllinkVidEmbedPlugin
    name = _('Video Embed')
    module = _("allink")
    form = AllinkVidEmbedPluginForm

    class Media:
        js = (
            get_files('djangocms_custom_admin_scripts')[0]['publicPath'],
        )
        css = {
            'all': (
                get_files('djangocms_custom_admin_style')[0]['publicPath'],

            )
        }

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': (
                    'video_id',
                    'video_service',
                )
            }),
            (_('Video settings'), {
                # 'classes': ('collapse',),
                'fields': (
                    'ratio',
                    'auto_start_enabled',
                    'allow_fullscreen_enabled',
                )
            }),
            (_('Advanced settings'), {
                'classes': ('collapse',),
                'fields': (
                    'attributes',
                    'project_css_classes',
                )
            }),
        ]
        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'djangocms_vid/embed/content.html'
        return template

@plugin_pool.register_plugin
class CMSAllinkVidFilePlugin(CMSPluginBase):
    model = AllinkVidFilePlugin
    name = _('Video File')
    module = _("allink")
    form = AllinkVidFilePluginForm

    class Media:
        js = (
            'build/djangocms_custom_admin_scripts.js',
        )
        css = {
            'all': (
                'build/djangocms_custom_admin_style.css',

            )
        }

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': (
                    'video_file',
                    'video_poster_image'
                )
            }),
            (_('Video settings'), {
                # 'classes': ('collapse',),
                'fields': (
                    'auto_start_enabled',
                    'video_muted_enabled',
                    'poster_only_on_mobile',
                    # 'allow_fullscreen_enabled',
                )
            }),
            (_('Advanced settings'), {
                'classes': ('collapse',),
                'fields': (
                    'attributes',
                    'project_css_classes',
                )
            }),
        ]
        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'djangocms_vid/file/content.html'
        return template
