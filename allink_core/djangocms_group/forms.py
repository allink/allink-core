# -*- coding: utf-8 -*-
from django import forms
from .models import AllinkGroupContainerPlugin, AllinkGroupPlugin


class AllinkGroupContainerPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkGroupContainerPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')


class AllinkGroupPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkGroupPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
