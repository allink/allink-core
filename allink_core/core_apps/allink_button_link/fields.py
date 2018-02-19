# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django import forms

from allink_core.core.models import choices
from allink_core.core_apps.allink_button_link import widgets


class Context(forms.fields.ChoiceField):
    widget = widgets.Context
    CHOICES = choices.CONTEXT_CHOICES
    DEFAULT = choices.CONTEXT_DEFAULT

    def __init__(self, *args, **kwargs):
        if 'choices' not in kwargs:
            kwargs['choices'] = self.CHOICES
        if 'initial' not in kwargs:
            kwargs['initial'] = self.DEFAULT
        kwargs.pop('coerce', None)
        kwargs.pop('max_length', None)
        kwargs.pop('widget', None)
        kwargs['widget'] = self.widget
        super(Context, self).__init__(*args, **kwargs)


class Size(forms.fields.ChoiceField):
    widget = widgets.Size
    CHOICES = choices.SIZE_CHOICES
    DEFAULT = 'md'

    def __init__(self, *args, **kwargs):
        if 'choices' not in kwargs:
            kwargs['choices'] = self.CHOICES
        if 'initial' not in kwargs:
            kwargs['initial'] = self.DEFAULT
        kwargs.pop('coerce', None)
        kwargs.pop('max_length', None)
        kwargs.pop('widget', None)
        kwargs['widget'] = self.widget
        super(Size, self).__init__(*args, **kwargs)


class LinkOrButton(forms.fields.ChoiceField):
    widget = widgets.LinkOrButton
    CHOICES = (
        ('lnk', 'Link'),
        ('btn', 'Button'),
    )
    DEFAULT = 'lnk'

    def __init__(self, *args, **kwargs):
        if 'choices' not in kwargs:
            kwargs['choices'] = self.CHOICES
        if 'initial' not in kwargs:
            kwargs['initial'] = self.DEFAULT
        kwargs.pop('coerce', None)
        kwargs.pop('max_length', None)
        kwargs.pop('widget', None)
        kwargs['widget'] = self.widget
        super(LinkOrButton, self).__init__(*args, **kwargs)
