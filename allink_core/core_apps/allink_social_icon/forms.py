# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from allink_core.core.utils import get_additional_choices
from allink_core.core_apps.allink_social_icon.models import AllinkSocialIconContainerPlugin, AllinkSocialIconPlugin


class AllinkSocialIconContainerPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkSocialIconContainerPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkSocialIconContainerPluginForm, self).__init__(*args, **kwargs)
        if get_additional_choices('SOCIAL_ICON_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label=_(u'Predifined variations for Social Icon Plugin'),
                choices=get_additional_choices('SOCIAL_ICON_CSS_CLASSES'),
                required=False,
            )

class AllinkSocialIconPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkSocialIconPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
