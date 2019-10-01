# -*- coding: utf-8 -*-
from functools import partial
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.fields import PositiveIntegerField
from django.utils.translation import ugettext as _

from cms.models.pluginmodel import CMSPlugin

from allink_core.core.forms import fields


# Add an app namespace to related_name to avoid field name clashes
# with any other plugins that have a field with the same name as the
# lowercase of the class name of this model.
# https://github.com/divio/django-cms/issues/5030
CMSPluginField = partial(
    models.OneToOneField,
    to=CMSPlugin,
    on_delete=models.CASCADE,
    related_name='%(app_label)s_%(class)s',
    parent_link=True,
)


class Icon(models.CharField):
    default_field_class = fields.Icon
    south_field_class = 'django.db.models.fields.CharField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = 'Icon'
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'default' not in kwargs:
            kwargs['default'] = self.default_field_class.DEFAULT
        super(Icon, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(Icon, self).formfield(**defaults)


class ZipCodeField(PositiveIntegerField):
    default_validators = [MaxValueValidator(9999)]
    default_field_class = fields.ZipCode
    description = 'Zip Code Field'

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(ZipCodeField, self).formfield(**defaults)
