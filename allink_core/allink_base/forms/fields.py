# -*- coding: utf-8 -*-

from django import forms

from . import widgets

class Classes(forms.fields.CharField):
    widget = forms.widgets.Textarea


class Icon(forms.fields.CharField):
    widget = widgets.Icon
    DEFAULT = ''

    def __init__(self, *args, **kwargs):
        if 'initial' not in kwargs:
            kwargs['initial'] = self.DEFAULT
        kwargs.pop('coerce', None)
        kwargs.pop('max_length', None)
        kwargs.pop('widget', None)
        kwargs['widget'] = self.widget
        super(Icon, self).__init__(*args, **kwargs)


class ZipCode(forms.fields.IntegerField):
    widget = forms.widgets.NumberInput(attrs={'max_length': 4})


