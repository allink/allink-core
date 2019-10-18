# -*- coding: utf-8 -*-
from django import forms
from cms.plugin_base import CMSPluginBase
from webpack_loader.utils import get_files

from cms.plugin_pool import plugin_pool

from allink_core.core.utils import get_additional_choices, get_ratio_choices
from allink_core.core_apps.allink_video.models import AllinkVideoFilePlugin, AllinkVideoEmbedPlugin
from allink_core.core.admin.mixins import AllinkMediaAdminMixin


class AllinkVideoEmbedPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkVideoEmbedPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkVideoEmbedPluginForm, self).__init__(*args, **kwargs)
        if get_additional_choices('VID_EMBED_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label='Predifined variations for Video Plugin',
                choices=get_additional_choices('VID_EMBED_CSS_CLASSES'),
                required=False,
            )
        self.fields['ratio'] = forms.CharField(
            label='Ratio',
            help_text='This option overrides the default ratio setting for embeded videos.',
            widget=forms.Select(choices=get_ratio_choices()),
            required=False,
        )


class AllinkVideoFilePluginForm(forms.ModelForm):

    class Meta:
        model = AllinkVideoFilePlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkVideoFilePluginForm, self).__init__(*args, **kwargs)
        if get_additional_choices('VID_FILE_CSS_CLASSES').__len__() != 0:
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label='Predifined variations for Video Plugin',
                choices=get_additional_choices('VID_FILE_CSS_CLASSES'),
                required=False,
            )


@plugin_pool.register_plugin
class CMSAllinkVideoEmbedPlugin(AllinkMediaAdminMixin, CMSPluginBase):
    model = AllinkVideoEmbedPlugin
    name = 'Video Embed'
    module = 'Generic'
    form = AllinkVideoEmbedPluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': (
                    'video_id',
                    'video_service',
                )
            }),
            ('Video settings', {
                # 'classes': ('collapse',),
                'fields': (
                    'ratio',
                    'auto_start_enabled',
                    'allow_fullscreen_enabled',
                )
            }),
            ('Advanced settings', {
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
class CMSAllinkVideoFilePlugin(AllinkMediaAdminMixin, CMSPluginBase):
    model = AllinkVideoFilePlugin
    name = 'Video File'
    module = 'Generic'
    form = AllinkVideoFilePluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': (
                    'video_file',
                    'video_poster_image'
                )
            }),
            ('Video settings', {
                # 'classes': ('collapse',),
                'fields': (
                    'auto_start_enabled',
                    'auto_start_mobile_enabled',
                    'video_muted_enabled',
                    'poster_only_on_mobile',
                    # 'allow_fullscreen_enabled',
                )
            }),
            ('Advanced settings', {
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
