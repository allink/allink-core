# -*- coding: utf-8 -*-
from django import forms
from .models import AllinkTermsPlugin


class AllinkTermsPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkTermsPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
