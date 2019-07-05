# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from webpack_loader.utils import get_files

from cms.plugin_pool import plugin_pool

from allink_core.core.utils import get_additional_choices, get_ratio_choices
from allink_core.core_apps.allink_video.models import AllinkVideoFilePlugin, AllinkVideoEmbedPlugin


class AllinkVideoEmbedPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkVideoEmbedPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkVideoEmbedPluginForm, self).__init__(*args, **kwargs)
        if get_additional_choices('VID_EMBED_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label=_('Predifined variations for Video Plugin'),
                choices=get_additional_choices('VID_EMBED_CSS_CLASSES'),
                required=False,
            )
        self.fields['ratio'] = forms.CharField(
            label=_('Ratio'),
            help_text=_('This option overrides the default ratio setting for embeded videos.'),
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
                label=_('Predifined variations for Video Plugin'),
                choices=get_additional_choices('VID_FILE_CSS_CLASSES'),
                required=False,
            )


@plugin_pool.register_plugin
class CMSAllinkVideoEmbedPlugin(CMSPluginBase):
    model = AllinkVideoEmbedPlugin
    name = _('Video Embed')
    module = _('Generic')
    form = AllinkVideoEmbedPluginForm

    class Media:
        js = (
            get_files('djangocms_custom_admin')[1]['publicPath'],
        )
        css = {
            'all': (
                get_files('djangocms_custom_admin')[0]['publicPath'],

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
    module = _('Generic')
    form = AllinkVideoFilePluginForm

    class Media:
        js = (get_files('djangocms_custom_admin')[1]['publicPath'], )
        css = {
            'all': (get_files('djangocms_custom_admin')[0]['publicPath'], )
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
