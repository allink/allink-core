# -*- coding: utf-8 -*-

from __future__ import unicode_literals
# import warnings

from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields.related import (
    ForeignKey,
    ManyToManyField,
    OneToOneField
)
from django.forms.models import ModelChoiceField, ModelMultipleChoiceField
from django.utils.safestring import mark_safe

# For South, where used.
try:
    from south.modelsinspector import add_introspection_rules
except:  # pragma: no cover
    add_introspection_rules = False

from aldryn_categories.fields import CategoryModelChoiceField, CategoryForeignKey, CategoryOneToOneField, CategoryMultipleChoiceField, CategoryManyToManyField

from .models import AllinkCategory as Category


class CategoryModelChoiceField(CategoryModelChoiceField):
    pass

class CategoryForeignKey(CategoryForeignKey):
    pass

class CategoryOneToOneField(CategoryOneToOneField):
   pass

class CategoryMultipleChoiceField(CategoryMultipleChoiceField):
    pass

class CategoryManyToManyField(CategoryManyToManyField):
    pass
