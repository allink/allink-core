# -*- coding: utf-8 -*-
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from parler.forms import TranslatableModelForm


class AllinkCategoryAdminForm(TranslatableModelForm):
    """
    TranslatableModelForm used in combination with AllinkCategoryModel
    """
    def __init__(self, *args, **kwargs):
        super(AllinkCategoryAdminForm, self).__init__(*args, **kwargs)
        # if app uses categories, populate 'categories' field
        if self.instance.__class__.get_can_have_categories():
            self.fields['categories'] = forms.ModelMultipleChoiceField(
                label='Categories',
                widget=FilteredSelectMultiple(
                    verbose_name='Categories',
                    is_stacked=True
                ),
                required=True,
                queryset=self.instance.get_relevant_categories()
            )
