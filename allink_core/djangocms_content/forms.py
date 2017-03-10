# -*- coding: utf-8 -*-
from django import forms
from .models import AllinkContentPlugin, AllinkContentColumnPlugin


class AllinkContentPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkContentPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    class Media:
        js = ('/static/djangocms_content/js/djangocms_content.js', )

    def __init__(self, *args, **kwargs):
        super(AllinkContentPluginForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            if kwargs.get('instance').numchild != 0:
                self.fields['template'].required = False
                self.fields['template'].widget.attrs['disabled'] = True


class AllinkContentColumnPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkContentColumnPlugin
        exclude = ('title', 'page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkContentColumnPluginForm, self).__init__(*args, **kwargs)
        parent_column_amount = AllinkContentPlugin.COLUMN_AMOUNT[kwargs.get('instance').template]
        self.fields['order_mobile'].widget = forms.Select(choices=enumerate(range(parent_column_amount)))
