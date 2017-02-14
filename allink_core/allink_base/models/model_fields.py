# -*- coding: utf-8 -*-
from django import forms
from functools import partial
from django.db import models
from django.utils.translation import ugettext as _
from django.core.validators import MaxValueValidator
from cms.models.pluginmodel import CMSPlugin
from ..forms import fields


# first_name =
class FirstName(models.CharField):
    south_field_class = 'django.db.models.fields.CharField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = _(u'First Name')
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'null' not in kwargs:
            kwargs['null'] = True
        super(FirstName, self).__init__(*args, **kwargs)


# last_name =
class LastName(models.CharField):
    south_field_class = 'django.db.models.fields.CharField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = _(u'Last Name')
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'null' not in kwargs:
            kwargs['null'] = True
        super(LastName, self).__init__(*args, **kwargs)


# email =
class Email(models.CharField):
    south_field_class = 'django.db.models.fields.CharField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = _(u'Email')
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'null' not in kwargs:
            kwargs['null'] = True
        super(Email, self).__init__(*args, **kwargs)


# message =
class Message(models.CharField):
    south_field_class = 'django.db.models.fields.CharField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = _(u'Message')
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'null' not in kwargs:
            kwargs['null'] = True
        super(Message, self).__init__(*args, **kwargs)


# street =
class Street(models.CharField):
    south_field_class = 'django.db.models.fields.CharField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = _(u'Street')
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'null' not in kwargs:
            kwargs['null'] = True
        super(Street, self).__init__(*args, **kwargs)


# zip_code =
class ZipCode(models.PositiveIntegerField):
    south_field_class = 'django.db.models.fields.PositiveIntegerField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = _(u'Zip Code')
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'null' not in kwargs:
            kwargs['null'] = True
        if 'validators' not in kwargs:
            kwargs['validators'] = [MaxValueValidator(9999)]
        super(ZipCode, self).__init__(*args, **kwargs)


# place =
class Place(models.CharField):
    south_field_class = 'django.db.models.fields.CharField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = _(u'Place')
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'null' not in kwargs:
            kwargs['null'] = True
        super(Place, self).__init__(*args, **kwargs)



# Add an app namespace to related_name to avoid field name clashes
# with any other plugins that have a field with the same name as the
# lowercase of the class name of this model.
# https://github.com/divio/django-cms/issues/5030
CMSPluginField = partial(
    models.OneToOneField,
    to=CMSPlugin,
    related_name='%(app_label)s_%(class)s',
    parent_link=True,
)

class Classes(models.TextField):
    default_field_class = fields.Classes
    south_field_class = 'django.db.models.fields.TextField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = _(u'Css Classes')
        if 'blank' not in kwargs:
            kwargs['blank'] = True
        if 'default' not in kwargs:
            kwargs['default'] = ''
        if 'help_text' not in kwargs:
            kwargs['help_text'] = _('Space separated classes that are added to '
                'the class. See <a href="http://getbootstrap.com/css/" '
                'target="_blank">Bootstrap 3 documentation</a>.')
        super(Classes, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': self.default_field_class,
        }
        defaults.update(kwargs)
        return super(Classes, self).formfield(**defaults)


class Icon(models.CharField):
    default_field_class = fields.Icon
    south_field_class = 'django.db.models.fields.CharField'

    def __init__(self, *args, **kwargs):
        if 'verbose_name' not in kwargs:
            kwargs['verbose_name'] = _(u'Icon')
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
