# -*- coding: utf-8 -*-
from django import forms
from .models import AllinkButtonLinkContainerPlugin, AllinkButtonLinkPlugin


class AllinkButtonLinkContainerPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkButtonLinkContainerPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')


class AllinkButtonLinkPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkButtonLinkPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
