# -*- coding: utf-8 -*-

from django import forms
from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from cms.apphook_pool import apphook_pool

from allink_core.allink_base.forms import widgets
from allink_core.allink_base.utils import get_project_color_choices


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
    widget = forms.widgets.NumberInput(attrs={'maxlength': 4})


class ColorField(forms.fields.CharField):

    def __init__(self, *args, **kwargs):
        super(ColorField, self).__init__(*args, **kwargs)
        default = None
        for key, val in get_project_color_choices().items():
            if val == self.initial:
                default = key
                break
        self.widget = widgets.SpectrumColorPicker(default=default)

    def clean(self, value):
        if value:
            try:
                value = get_project_color_choices()[value]
            except KeyError:
                raise ValidationError(_('Please choose a predefined color.'))
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        return value


# in progress
class SelectLinkField(forms.fields.ChoiceField):

    def __init__(self, required=True, widget=None, label=None,
                 initial=None, help_text='', *args, **kwargs):
        super(forms.fields.ChoiceField, self).__init__(
            required=required, widget=widget, label=label, initial=initial,
            help_text=help_text, *args, **kwargs
        )
        self.choices = self.get_page_and_app_choices()

    def get_page_and_app_choices(self):
        pass

        # in progress

        # link_apphooks = settings.PROJECT_LINK_APPHOOKS
        # cached_choices = cache.get('page_app_link_choices', None)
        # if cached_choices:
        #     return cached_choices

        # choices = []
        # for apphook, url_names in link_apphooks:
        #     if apphook == 'Page':



        # cache.set('page_app_link_choices', choices, 60)
        # return choices
