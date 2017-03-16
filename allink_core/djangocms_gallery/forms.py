# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import AllinkGalleryPlugin, AllinkGalleryImagePlugin


class AllinkGalleryPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkGalleryPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkGalleryPluginForm, self).__init__(*args, **kwargs)
        self.fields['ratio'] = forms.CharField(
            label=_(u'Ratio'),
            help_text=_(u'This option overrides the default settings for the gallery plugin.'),
            widget=forms.Select(choices=self.instance.get_ratio_choices()),
            required=False,
        )

class AllinkGalleryImagePluginForm(forms.ModelForm):

    class Meta:
        model = AllinkGalleryImagePlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
