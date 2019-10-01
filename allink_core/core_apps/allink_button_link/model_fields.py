# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models

from allink_core.core_apps.allink_button_link import fields


class LinkOrButton(models.CharField):
    default_field_class = fields.LinkOrButton
    south_field_class = 'django.db.models.fields.CharField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = 'Type'
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = False
        if 'default' not in kwargs:
            kwargs['default'] = self.default_field_class.DEFAULT
        super(LinkOrButton, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
            'choices_form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(LinkOrButton, self).formfield(**defaults)

    def get_choices(self, **kwargs):
        # if there already is a "blank" choice, don't add another
        # default blank choice
        if '' in dict(self.choices).keys():
            kwargs['include_blank'] = False
        return super(LinkOrButton, self).get_choices(**kwargs)


class Context(models.CharField):
    default_field_class = fields.Context
    south_field_class = 'django.db.models.fields.CharField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = 'Context'
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = False
        if 'default' not in kwargs:
            kwargs['default'] = self.default_field_class.DEFAULT
        super(Context, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
            'choices_form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(Context, self).formfield(**defaults)

    def get_choices(self, **kwargs):
        # if there already is a "blank" choice, don't add another
        # default blank choice
        if '' in dict(self.choices).keys():
            kwargs['include_blank'] = False
        return super(Context, self).get_choices(**kwargs)


class Size(models.CharField):
    default_field_class = fields.Size
    south_field_class = 'django.db.models.fields.CharField'

    def __init__(self, *args, **kwargs):
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'default' not in kwargs:
            kwargs['default'] = self.default_field_class.DEFAULT
        super(Size, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
            'choices_form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(Size, self).formfield(**defaults)

    def get_choices(self, **kwargs):
        # if there already is a "blank" choice, don't add another
        # default blank choice
        if '' in dict(self.choices).keys():
            kwargs['include_blank'] = False
        return super(Size, self).get_choices(**kwargs)


# TODO:
#   * btn-block, disabled
#   * pull-left, pull-right
#   * margins/padding
