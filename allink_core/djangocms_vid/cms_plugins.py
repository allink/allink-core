# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase

from cms.plugin_pool import plugin_pool
from allink_core.djangocms_vid.models import AllinkVidEmbedPlugin, AllinkVidFilePlugin
from allink_core.djangocms_vid.forms import AllinkVidEmbedPluginForm, AllinkVidFilePluginForm


@plugin_pool.register_plugin
class CMSAllinkVidEmbedPlugin(CMSPluginBase):
    model = AllinkVidEmbedPlugin
    name = _('Video Embed')
    module = _("allink")
    form = AllinkVidEmbedPluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': (
                    'video_id',
                    'video_service',
                )
            }),
            (_('Video settings'), {
                'classes': ('collapse',),
                'fields': (
                    'auto_start_enabled',
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


@plugin_pool.register_plugin
class CMSAllinkVidFilePlugin(CMSPluginBase):
    model = AllinkVidFilePlugin
    name = _('Video File')
    module = _("allink")
    form = AllinkVidFilePluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': (
                    'video_file',
                )
            }),
            (_('Video settings'), {
                'classes': ('collapse',),
                'fields': (
                    'auto_start_enabled',
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
