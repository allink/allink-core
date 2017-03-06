# -*- coding: utf-8 -*-
from django import forms
from .models import AllinkGalleryPlugin, AllinkGalleryImagePlugin


class AllinkGalleryPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkGalleryPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')


class AllinkGalleryImagePluginForm(forms.ModelForm):

    class Meta:
        model = AllinkGalleryImagePlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
