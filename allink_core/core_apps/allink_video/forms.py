# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
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
                label=_(u'Predifined variations for Video Plugin'),
                choices=get_additional_choices('VID_EMBED_CSS_CLASSES'),
                required=False,
            )
        self.fields['ratio'] = forms.CharField(
            label=_(u'Ratio'),
            help_text=_(u'This option overrides the default ratio setting for embeded videos.'),
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
                label=_(u'Predifined variations for Video Plugin'),
                choices=get_additional_choices('VID_FILE_CSS_CLASSES'),
                required=False,
            )
