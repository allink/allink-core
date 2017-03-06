# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from parler.admin import TranslatableAdmin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory, MoveNodeForm

from parler.forms import TranslatableModelForm

from .models import AllinkCategory


class AllinkCategoryForm(TranslatableModelForm, MoveNodeForm):
    model_names = forms.MultipleChoiceField(
        label=_(u'Project app'),
        help_text=_(u'Please specify the project-app which uses this categories.'),
        choices=settings.PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

#  TODO: add user is_superuser check! (or better after creating user grou/role concept!) -> dont allow "editors" to add/read/write/delete
@admin.register(AllinkCategory)
class AllinkCategoryAdmin(TranslatableAdmin, TreeAdmin):
    form = movenodeform_factory(AllinkCategory, form=AllinkCategoryForm)
    list_display = ('name', )
