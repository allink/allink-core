# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.conf import settings
from parler.admin import TranslatableAdmin
from django.http import HttpResponseRedirect

from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory, MoveNodeForm

from parler.forms import TranslatableModelForm

from allink_core.core.utils import get_additional_choices
from allink_core.core_apps.allink_categories.models import AllinkCategory


class AllinkCategoryForm(TranslatableModelForm, MoveNodeForm):
    model_names = forms.MultipleChoiceField(
        label='Project app',
        help_text=('Please specify the app which uses this categories. All apps specified in parent category '
                   'are automatically added.'),
        choices=settings.PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta():
        model = AllinkCategory
        fields = ('name', 'identifier', 'slug', 'logo', 'model_names')

    def __init__(self, *args, **kwargs):
        super(AllinkCategoryForm, self).__init__(*args, **kwargs)
        # hide model_names when
        if self.instance and not self.instance.is_root():
            self.fields['model_names'].widget = forms.MultipleHiddenInput()

        if get_additional_choices('PROJECT_CATEGORY_IDENTIFIERS'):
            self.fields['identifier'] = forms.ChoiceField(
                label='Identifier',
                help_text='Identifier used for backward reference on a app model. (e.g display category name '
                            'on People app, e.g Marketing)',
                choices=get_additional_choices('PROJECT_CATEGORY_IDENTIFIERS', blank=True),
                required=False,
            )


@admin.register(AllinkCategory)
class AllinkCategoryAdmin(TranslatableAdmin, TreeAdmin):
    form = movenodeform_factory(AllinkCategory, form=AllinkCategoryForm)
    list_display = ('name', )
    # fields = ('name',  'slug', 'model_names')

    def response_add(self, request, obj, post_url_continue=None):
        if obj.is_root():
            return HttpResponseRedirect("../%s" % obj.id)
        else:
            return super(AllinkCategoryAdmin, self).response_add(request, obj, post_url_continue=post_url_continue)
