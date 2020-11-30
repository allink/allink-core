# -*- coding: utf-8 -*-
import json

from django import forms
from django.core.cache import cache
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from cms.apphook_pool import apphook_pool
from cms.models import Page
import sortedm2m.fields

from allink_core.core.loading import get_model
from allink_core.core.forms import widgets
from allink_core.core.utils import get_project_color_choices


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
            if len(value) == 4:
                value = '#%s%s%s%s%s%s' % (value[1], value[1], value[2], value[2], value[3], value[3])
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
        self.choices = []

    def get_page_and_app_choices(self):
        link_apphooks = settings.PROJECT_LINK_APPHOOKS
        """
        Structure in Settings:
         OrderedDict([
        ('Page', []),
        ('NewsApphook', [{'detail': ('allink_apps.news.models.News', ['slug'])}]),
        .... ])
        """
        cached_choices = cache.get('page_app_link_choices', None)
        if cached_choices:
            return cached_choices

        choices = [(None, '---------')]
        set_cache = True
        for apphook, url_names in link_apphooks.items():
            if apphook == 'Page':
                subchoices = []
                subchoices += [(json.dumps({'page_id': p.id}), '%s %s' % ((p.node.depth - 1) * '---', p))
                               for p in Page.objects.filter(publisher_is_draft=False).order_by('node__path')]
                choices.append(('%s' % 'pages'.upper(), subchoices))

            else:
                try:
                    subchoices = []
                    for p in Page.objects.filter(application_urls=apphook, publisher_is_draft=False):
                        for url_name, info in url_names.items():
                            get_model(info[0].split('.')[-3], info[0].split('.')[-1])
                            obj_model = get_model(info[0].split('.')[-3], info[0].split('.')[-1])
                            subchoices += [(json.dumps({'link_apphook_page_id': p.id, 'link_url_name': url_name,
                                                        'link_object_id': obj.id, 'link_url_kwargs': info[1],
                                                        'link_model': info[0]}), '%s (%s)'
                                            % (obj, p.application_namespace))
                                           for obj in obj_model.objects.all()]
                    choices.append((('%s' % apphook_pool.apps[apphook].app_name.upper()), subchoices))
                # on app load time
                except KeyError:
                    set_cache = False

        if set_cache:
            cache.set('page_app_link_choices', choices, 30)
        return choices


class SortedM2MFormField(sortedm2m.fields.SortedMultipleChoiceField):
    """
    Copied from https://github.com/divio/aldryn-common

    Copied because this package is no longer maintained.
    https://github.com/divio/aldryn-common/commit/6582754be67390d056d4aaa1f799c183e808c914

    """
    widget = widgets.SortedM2MWidget

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = self.widget
        super(SortedM2MFormField, self).__init__(*args, **kwargs)
