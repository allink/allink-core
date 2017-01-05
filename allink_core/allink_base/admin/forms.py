# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

from parler.forms import TranslatableModelForm

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
                required=False,
                queryset=AllinkCategory.objects.not_root().filter(
                    model_names__contains=[self.instance._meta.model_name]
                )
            )


class AllinkBaseAppContentPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkBaseAppContentPlugin
        fields = (
            'title',
            'categories',
            'template',
            'container_enabled',
            'bg_color',
            'items_per_row',
            'paginated_by',
            'pagination_type',
            'detail_link_text'
        )

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

        self.fields['template'] = forms.CharField(
            label=_(u'Template'),
            widget=forms.Select(choices=self.instance.get_templates()),
            required=True,
        )
