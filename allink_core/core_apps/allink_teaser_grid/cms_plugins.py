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

        if get_additional_choices('CONTENT_TITLE_CHOICES'):
            self.fields['title_size'] = forms.CharField(
                label='Section Title Size',
                widget=forms.Select(
                    choices=get_additional_choices('CONTENT_TITLE_CHOICES'),
                ),
                initial=settings.CONTENT_TITLE_CHOICES_DEFAULT,
                required=False,
            )
        else:
            self.fields['title_size'] = forms.CharField(widget=forms.HiddenInput(), required=False)

        if get_additional_choices('CONTENT_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label='Predefined variations',
                choices=get_additional_choices('CONTENT_CSS_CLASSES'),
                initial=get_additional_choices('INITIAL_CONTENT_CSS_CLASSES'),
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

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_teaser_grid/content.html'
        return template
