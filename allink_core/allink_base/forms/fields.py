# -*- coding: utf-8 -*-
import json
from importlib import import_module

from django import forms
from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from cms.apphook_pool import apphook_pool
from cms.models import Page

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
            required=required, widget=widgets.SearchSelectWidget(), label=label, initial=initial,
            help_text=help_text, *args, **kwargs
        )
        # self.choices = self.get_page_and_app_choices()

    def get_page_and_app_choices(self):
        # in progress

        link_apphooks = settings.PROJECT_LINK_APPHOOKS
        cached_choices = cache.get('page_app_link_choices', None)
        if cached_choices:
            return cached_choices

        choices = [(None, '---------')]
        set_cache = True
        for apphook, url_names in link_apphooks.items():
            if apphook == 'Page':
                choices.append((None, ('----%s----' % _('pages')).upper()))
                choices += [(json.dumps({'page_id': p.id}), '%s %s' % ((p.depth - 1) * '---', p)) for p in Page.objects.filter(publisher_is_draft=False)]

            # ('BlogApphook', [{'detail': ('allink_apps.blog.models.Blog', ['slug'])}])
            else:
                try:
                    choices.append((None, ''))
                    choices.append((None, ('----%s----' % apphook_pool.apps[apphook].app_name).upper()))
                    for p in Page.objects.filter(application_urls=apphook, publisher_is_draft=False):
                        for url_name, info in url_names.items():
                            obj_module = import_module(info[0][0])
                            obj_model = getattr(obj_module, info[0][1])
                            choices += [(json.dumps({'link_apphook_page_id': p.id, 'link_url_name': url_name, 'link_object_id': obj.id, 'link_url_kwargs': info[1]}), '%s (%s)' % (obj, p.application_namespace)) for obj in obj_model.objects.all()]
                # on app load time
                except KeyError:
                    set_cache = False

        if set_cache:
            cache.set('page_app_link_choices', choices, 30)
        return choices
