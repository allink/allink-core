# -*- coding: utf-8 -*-
from django import forms
from cms.plugin_base import CMSPluginBase
from webpack_loader.utils import get_files

from cms.plugin_pool import plugin_pool

from allink_core.core.utils import get_ratio_choices_orig, get_additional_choices, \
    get_project_color_choices, get_image_width_alias_choices
from allink_core.core_apps.allink_image.models import AllinkImagePlugin
from allink_core.core.forms.fields import ColorField
from allink_core.core.forms.fields import SelectLinkField
from allink_core.core.forms.mixins import AllinkInternalLinkFieldMixin
from allink_core.core.admin.mixins import AllinkMediaAdminMixin


class AllinkImagePluginForm(AllinkInternalLinkFieldMixin, forms.ModelForm):

    internal_link = SelectLinkField(label='Link Internal', required=False)

    class Meta:
        model = AllinkImagePlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
        widgets = {
            'caption_text': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(AllinkImagePluginForm, self).__init__(*args, **kwargs)
        self.fields['link_special'] = forms.CharField(
            label='Special Links',
            widget=forms.Select(choices=self.instance.get_link_special_choices()),
            required=False,
            help_text=('Important: In case the selected option is a <strong>form</strong>, make sure to '
                       'select <strong>Lightbox (Forms)</strong> from the <strong>link target</strong> options '
                       'for best user experience.'),
        )
        self.fields['ratio'] = forms.CharField(
            label='Ratio',
            help_text=('This option overrides the default image ratio set for images in a colum of a '
                       'content section.'),
            widget=forms.Select(choices=get_ratio_choices_orig()),
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
        if get_project_color_choices():
            self.fields['bg_color'] = ColorField(
                label='Set a predefined background color',
                required=False,
            )

        if get_additional_choices('IMAGE_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label='Predifined variations',
                choices=get_additional_choices('IMAGE_CSS_CLASSES'),
                required=False,
            )


@plugin_pool.register_plugin
class CMSAllinkImagePlugin(AllinkMediaAdminMixin, CMSPluginBase):
    model = AllinkImagePlugin
    name = 'Image'
    module = 'Generic'
    form = AllinkImagePluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': [
                    'picture',
                    'ratio',
                    'project_css_classes',
                    'icon_enabled',
                    'bg_enabled',

                ]
            }),
            ('Additional settings', {
                'classes': ('collapse',),
                'fields': [
                    'caption_text',
                    'attributes',
                ]
            }),
            ('Link settings', {
                'classes': ('collapse',),
                'fields': (
                    'internal_link',
                    'link_url',
                    ('link_mailto', 'link_phone'),
                    ('link_anchor', 'link_special'),
                    'link_file',
                    'link_target',
                )
            }),
        ]

        if get_project_color_choices():
            fieldsets[0][1].get('fields').append('bg_color')
        if get_image_width_alias_choices():
            fieldsets[1][1].get('fields').append('width_alias')
        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_image/content.html'
        return template

    @classmethod
    def get_render_queryset(cls):
        return cls.model._default_manager.all()
