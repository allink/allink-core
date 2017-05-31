# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from allink_core.allink_base.utils import get_additional_choices, get_ratio_choices
from allink_core.djangocms_vid.models import AllinkVidFilePlugin, AllinkVidEmbedPlugin


class AllinkVidEmbedPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkVidEmbedPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkVidEmbedPluginForm, self).__init__(*args, **kwargs)
        if get_additional_choices('VID_EMBED_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                label=_(u'Predifined variations for Video Plugin'),
                help_text=_(u'Instructions: Single selection is made by clicking on an option. Multiple selections are achieved by pressing and holding down the Command-key (Mac) or Control-Key (Windows) <strong>and</strong> clicking the options you would like to apply.'),
                choices=get_additional_choices('VID_EMBED_CSS_CLASSES'),
                required=False,
            )
        self.fields['ratio'] = forms.CharField(
            label=_(u'Ratio'),
            help_text=_(u'This option overrides the default ratio setting for embeded videos.'),
            widget=forms.Select(choices=get_ratio_choices()),
            required=False,
        )

class AllinkVidFilePluginForm(forms.ModelForm):

    class Meta:
        model = AllinkVidFilePlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkVidFilePluginForm, self).__init__(*args, **kwargs)
        if get_additional_choices('VID_FILE_CSS_CLASSES').__len__() != 0:
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                label=_(u'Predifined variations for Video Plugin'),
                help_text=_(u'Instructions: Single selection is made by clicking on an option. Multiple selections are achieved by pressing and holding down the Command-key (Mac) or Control-Key (Windows) <strong>and</strong> clicking the options you would like to apply.'),
                choices=get_additional_choices('VID_FILE_CSS_CLASSES'),
                required=False,
            )
