# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import AllinkVidPlugin


class AllinkVidPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkVidPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
        widgets = {
            'caption_text': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super(AllinkVidPluginForm, self).__init__(*args, **kwargs)
        self.fields['template'] = forms.CharField(
            label=_(u'Template'),
            widget=forms.Select(choices=self.instance.get_templates()),
            required=True,
        )
        self.fields['ratio'] = forms.CharField(
            label=_(u'Ratio'),
            help_text=_(u'This option overrides the default settings for the content plugin.'),
            widget=forms.Select(choices=self.instance.get_ratio_choices()),
            required=False,
        )
