# -*- coding: utf-8 -*-
from django import forms
from django.utils.html import strip_tags

from django.conf import settings
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from webpack_loader.utils import get_files
from allink_core.core.utils import get_ratio_choices, get_additional_choices, get_image_width_alias_choices
from allink_core.core_apps.allink_gallery.models import AllinkGalleryPlugin, AllinkGalleryImagePlugin
from allink_core.core.loading import get_model
from allink_core.core.admin.mixins import AllinkMediaAdminMixin

Config = get_model('config', 'Config')


class AllinkGalleryPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkGalleryPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkGalleryPluginForm, self).__init__(*args, **kwargs)
        self.fields['ratio'] = forms.CharField(
            label='Ratio',
            help_text='This option overrides the default settings for the gallery plugin.',
            widget=forms.Select(choices=get_ratio_choices()),
            required=False,
        )
        self.fields['template'] = forms.CharField(
            label='Template',
            widget=forms.Select(choices=self.instance.get_templates()),
            required=True,
        )
        if get_additional_choices('GALLERY_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label='Predifined variations',
                choices=get_additional_choices('GALLERY_CSS_CLASSES'),
                required=False,
            )

        if get_image_width_alias_choices():
            self.fields['width_alias'] = forms.CharField(
                label='Width Alias',
                help_text=('This option overrides the default image width_alias set for images in a column of a '
                           'content section.'),
                widget=forms.Select(choices=get_image_width_alias_choices()),
                required=False,
            )


class AllinkGalleryImagePluginForm(forms.ModelForm):

    class Meta:
        model = AllinkGalleryImagePlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def clean(self):
        cleaned_data = super(AllinkGalleryImagePluginForm, self).clean()
        form_data = self.cleaned_data
        text_length = len(strip_tags(form_data['text']))
        max_length = settings.ALLINK_GALLERY_PLUGIN_CAPTION_TEXT_MAX_LENGTH

        if max_length and text_length > max_length:
            self.add_error(
                'text', 'There are only {} characters allowed in text field. Currently there are {} characters.'
                .format(max_length, text_length))

        return cleaned_data


@plugin_pool.register_plugin
class CMSAllinkGalleryPlugin(AllinkMediaAdminMixin, CMSPluginBase):
    model = AllinkGalleryPlugin
    name = 'Gallery'
    module = 'Generic'
    allow_children = True
    child_classes = ['CMSAllinkGalleryImagePlugin']
    form = AllinkGalleryPluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'template',
                    'folder',
                ),
            }),
            ('Slider Options', {
                'fields': [
                    'fullscreen_enabled',
                    'counter_enabled',
                    'auto_start_enabled',
                    'ratio',
                ]
            }),
            ('Advanced Options', {
                'classes': ('collapse',),
                'fields': (
                    'project_css_classes',
                )
            })
        )

        if get_image_width_alias_choices():
            fieldsets[1][1].get('fields').append('width_alias')

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_gallery/{}/content.html'.format(instance.template)
        return template


@plugin_pool.register_plugin
class CMSAllinkGalleryImagePlugin(AllinkMediaAdminMixin, CMSPluginBase):
    model = AllinkGalleryImagePlugin
    name = 'Gallery Image'
    module = 'Generic'
    allow_children = False
    form = AllinkGalleryImagePluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'image',
                    'title',
                    'text',
                ),
            }),
        )

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_gallery/{}/item.html'.format(instance.template)
        return template
