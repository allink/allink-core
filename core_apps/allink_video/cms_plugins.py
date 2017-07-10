# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from webpack_loader.utils import get_files

from cms.plugin_pool import plugin_pool
from allink_core.core_apps.allink_video.models import AllinkVideoEmbedPlugin, AllinkVideoFilePlugin
from allink_core.core_apps.allink_video.forms import AllinkVideoEmbedPluginForm, AllinkVideoFilePluginForm


@plugin_pool.register_plugin
class CMSAllinkVideoEmbedPlugin(CMSPluginBase):
    model = AllinkVideoEmbedPlugin
    name = _('Video Embed')
    module = _("allink")
    form = AllinkVideoEmbedPluginForm

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
        template = 'allink_video/embed/content.html'
        return template

@plugin_pool.register_plugin
class CMSAllinkVideoFilePlugin(CMSPluginBase):
    model = AllinkVideoFilePlugin
    name = _('Video File')
    module = _("allink")
    form = AllinkVideoFilePluginForm

    class Media:
        js = (get_files('djangocms_custom_admin')[0]['publicPath'], )
        css = {
            'all': (get_files('djangocms_custom_admin')[1]['publicPath'], )
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
        template = 'allink_video/file/content.html'
        return template
