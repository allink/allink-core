# -*- coding: utf-8 -*-
from django import forms
from .models import AllinkSocialIconContainerPlugin, AllinkSocialIconPlugin


class AllinkSocialIconContainerPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkSocialIconContainerPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')


class AllinkSocialIconPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkSocialIconPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
