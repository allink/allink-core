# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from parler.admin import TranslatableAdmin

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory, MoveNodeForm

from parler.forms import TranslatableModelForm

from allink_core.allink_categories.models import AllinkCategory


class AllinkCategoryForm(TranslatableModelForm, MoveNodeForm):
    model_names = forms.MultipleChoiceField(
        label=_(u'Project app'),
        help_text=_(u'Please specify the app which uses this categories. All apps specified in parent category are automatically added.'),
        choices=settings.PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta():
        model = AllinkCategory
        fields = ('name', 'slug', 'model_names')

    def __init__(self, *args, **kwargs):
        super(AllinkCategoryForm, self).__init__(*args, **kwargs)
        if self.instance and not self.instance.model_names and self.instance.get_parent() and self.instance.get_parent().model_names:
            self.instance.model_names = self.instance.get_parent().model_names
            super(AllinkCategoryForm, self).__init__(*args, **kwargs)


#  TODO: add user is_superuser check! (or better after creating user grou/role concept!) -> dont allow "editors" to add/read/write/delete
@admin.register(AllinkCategory)
class AllinkCategoryAdmin(TranslatableAdmin, TreeAdmin):
    form = movenodeform_factory(AllinkCategory, form=AllinkCategoryForm)
    list_display = ('name', )
    # fields = ('name',  'slug', 'model_names')
