# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

from parler.forms import TranslatableModelForm

from allink_core.allink_base.utils import get_additional_choices
from allink_core.allink_categories.models import AllinkCategory
from allink_core.allink_base.models import AllinkBaseAppContentPlugin

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
                queryset=AllinkCategory.objects.not_root().filter(
                    model_names__contains=[self.instance._meta.model_name]
                )
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
                queryset=AllinkCategory.objects.not_root().filter(
                    model_names__contains=[self.instance._meta.model_name]
                )
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
                queryset=AllinkCategory.objects.not_root().filter(
                    model_names__contains=[self._meta.model.data_model._meta.model_name]
                )
            )
            self.fields['categories_and'] = forms.ModelMultipleChoiceField(
                label=_(u'Categories (AND operator)'),
                widget=FilteredSelectMultiple(
                    verbose_name=_(u'Categories'),
                    is_stacked=True
                ),
                help_text=_(u'Use this field if you want to further restrict your result set. This option allows you to create a conjunction between the first set of categories in field "Categories" and the ones specified here.'),
                required=False,
                queryset=AllinkCategory.objects.not_root().filter(
                    model_names__contains=[self._meta.model.data_model._meta.model_name]
                )
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
                queryset=AllinkCategory.objects.not_root().filter(
                model_names__contains=[self._meta.model.data_model._meta.model_name]
                )
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
        self.fields['bg_color'] = forms.CharField(
            label=_(u'Background color'),
            widget=forms.Select(choices=self.instance.get_project_color_choices()),
            required=False,
        )
        if get_additional_choices('PROJECT_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                label=_(u'Predifined css classes'),
                choices=get_additional_choices('PROJECT_CSS_CLASSES'),
                required=False,
            )
        self.fields['manual_ordering'] = forms.CharField(
            label=_(u'Ordering'),
            required=False,
            widget=forms.Select(choices=self.instance.get_ordering_choices())
        )
