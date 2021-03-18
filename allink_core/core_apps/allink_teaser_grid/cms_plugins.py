# -*- coding: utf-8 -*-
from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from django import forms
from django.conf import settings
from allink_core.core.utils import get_additional_choices

from .models import AllinkTeaserGridContainerPlugin


class AllinkTeaserGridContainerPluginForm(forms.ModelForm):
    class Meta:
        model = AllinkTeaserGridContainerPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkTeaserGridContainerPluginForm, self).__init__(*args, **kwargs)

        if get_additional_choices('CONTENT_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label='Predefined variations',
                choices=AllinkTeaserGridContainerPlugin.SECTION_CSS_CLASSES,
                initial=AllinkTeaserGridContainerPlugin.SECTION_CSS_CLASSES_INITIAL,
                required=False,
            )

            self.fields['project_css_spacings_top_bottom'] = forms.ChoiceField(
                label='Spacings top & bottom',
                choices=get_additional_choices('CONTENT_SPACINGS', blank=True),
                required=False,
            )

            self.fields['project_css_spacings_top'] = forms.ChoiceField(
                label='Spacings top',
                choices=get_additional_choices('CONTENT_SPACINGS', blank=True),
                required=False,
            )

            self.fields['project_css_spacings_bottom'] = forms.ChoiceField(
                label='Spacings bottom',
                choices=get_additional_choices('CONTENT_SPACINGS', blank=True),
                required=False,
            )


@plugin_pool.register_plugin
class CMSAllinkTeaserGridContainerPlugin(CMSPluginBase):
    model = AllinkTeaserGridContainerPlugin
    name = 'Teaser Grid'
    module = 'allink modules'
    allow_children = True
    child_classes = ['CMSAllinkTeaserPlugin']
    form = AllinkTeaserGridContainerPluginForm

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'template',
                'column_order',
            ),
        }),
        ('Spacings', {
            'fields': [
                'project_css_spacings_top_bottom',
                'project_css_spacings_top',
                'project_css_spacings_bottom',
            ]
        }),
        ('Section Options', {
            'classes': ('collapse',),
            'fields': [
                'project_css_classes',
                'anchor',
            ]
        }),
    )

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_teaser_grid/content.html'
        return template
