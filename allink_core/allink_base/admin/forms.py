# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

from parler.forms import TranslatableModelForm

from allink_core.allink_base.utils import get_additional_choices, get_project_color_choices
from allink_core.allink_base.models import AllinkBaseAppContentPlugin
from allink_core.allink_base.forms.fields import ColorField


class AllinkBaseAdminForm(TranslatableModelForm):

    def __init__(self, *args, **kwargs):
        super(AllinkBaseAdminForm, self).__init__(*args, **kwargs)
        # if app uses categories, populate 'categories' field
        if self.instance.__class__.get_can_have_categories():
            self.fields['categories'] = forms.ModelMultipleChoiceField(
                label=_(u'Categories'),
                widget=FilteredSelectMultiple(
                    verbose_name=_(u'Categories'),
                    is_stacked=True
                ),
                required=True,
                queryset=self.instance.get_relevant_categories()
            )
            self.fields['category_navigation'] = forms.ModelMultipleChoiceField(
                label=_(u'Categories for Navigation'),
                widget=FilteredSelectMultiple(
                    verbose_name=_(u'Categories for Navigation'),
                    is_stacked=True
                ),
                help_text=_(
                    u'You can explicitly define the categories for the category navigation here. This will override the automatically set of categories. (From "Filter & Ordering" but not from the "Manual entries")'),
                required=False,
                queryset=self.instance.get_relevant_categories()
            )


class AllinkBaseAppContentPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkBaseAppContentPlugin
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(AllinkBaseAppContentPluginForm, self).__init__(*args, **kwargs)
        # if app uses categories, populate 'categories' field
        if self.instance.get_app_can_have_categories():
            self.fields['categories'] = forms.ModelMultipleChoiceField(
                label=_(u'Categories'),
                widget=FilteredSelectMultiple(
                    verbose_name=_(u'Categories'),
                    is_stacked=True
                ),
                required=False,
                queryset=self.instance.data_model.get_relevant_categories()
            )
            self.fields['categories_and'] = forms.ModelMultipleChoiceField(
                label=_(u'Categories (AND operator)'),
                widget=FilteredSelectMultiple(
                    verbose_name=_(u'Categories'),
                    is_stacked=True
                ),
                help_text=_(u'Use this field if you want to further restrict your result set. This option allows you to create a conjunction between the first set of categories in field "Categories" and the ones specified here.'),
                required=False,
                queryset=self.instance.data_model.get_relevant_categories()
            )
            self.fields['category_navigation'] = forms.ModelMultipleChoiceField(
                label=_(u'Categories for Navigation'),
                widget=FilteredSelectMultiple(
                    verbose_name=_(u'Categories for Navigation'),
                    is_stacked=True
                ),
                help_text=_(
                    u'You can explicitly define the categories for the category navigation here. This will override the automatically set of categories. (From "Filter & Ordering" but not from the "Manual entries")'),
                required=False,
                queryset=self.instance.data_model.get_relevant_categories()
            )
        self.fields['filter_fields'] = forms.TypedMultipleChoiceField(
            label=_(u'Filter Fields'),
            help_text=_(u'A Select Dropdown will be displayed for this Fields.'),
            choices=((field[0], field[1]['verbose']) for field in self.instance.FILTER_FIELD_CHOICES),
            widget=forms.CheckboxSelectMultiple,
            required=False,
        )
        self.fields['template'] = forms.CharField(
            label=_(u'Template'),
            widget=forms.Select(choices=self.instance.get_templates()),
            required=True,
        )
        self.fields['bg_color'] = ColorField(
            label=_(u'Background color'),
            required=False,
        )
        if get_additional_choices('PROJECT_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                label=_(u'Predifined css classes'),
                help_text=_(u'Instructions: Single selection is made by clicking on an option. Multiple selections are achieved by pressing and holding down the Command-key (Mac) or Control-Key (Windows) <strong>and</strong> clicking the options you would like to apply.'),
                choices=get_additional_choices('PROJECT_CSS_CLASSES'),
                required=False,
            )
        self.fields['manual_ordering'] = forms.CharField(
            label=_(u'Ordering'),
            required=False,
            widget=forms.Select(choices=self.instance.get_ordering_choices())
        )
