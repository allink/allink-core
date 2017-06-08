# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from allink_core.allink_base.utils import get_additional_choices
from allink_core.allink_base.forms.fields import ColorField
from allink_core.djangocms_content.models import AllinkContentPlugin, AllinkContentColumnPlugin


class AllinkContentPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkContentPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkContentPluginForm, self).__init__(*args, **kwargs)
        self.fields['template'] = forms.CharField(
            label=_(u'Template'),
            widget=forms.Select(choices=self.instance.get_template_choices()),
            required=True,
        )
        self.fields['bg_color'] = ColorField(
            label=_(u'Background color'),
            required=False,
        )
        if get_additional_choices('CONTENT_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                label=_(u'Predifined variations'),
                help_text=_(u'Instructions: Single selection is made by clicking on an option. Multiple selections are achieved by pressing and holding down the Command-key (Mac) or Control-Key (Windows) <strong>and</strong> clicking the options you would like to apply.'),
                choices=get_additional_choices('CONTENT_CSS_CLASSES'),
                required=False,
            )

    def clean(self):
        cleaned_data = super(AllinkContentPluginForm, self).clean()
        if self.has_changed():
            # if column count is not the same, dont allow template to change
            if self.instance.get_template_column_count(self.instance.template) != self.instance.get_template_column_count(cleaned_data['template']):
                self.add_error('template', _(u'You can only change the template if it has the same amount of columns as the previous template.'))
        return cleaned_data


class AllinkContentColumnPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkContentColumnPlugin
        exclude = ('title', 'page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkContentColumnPluginForm, self).__init__(*args, **kwargs)
        parent_column_amount = AllinkContentPlugin.get_template_column_count(kwargs.get('instance').template)
        self.fields['order_mobile'].widget = forms.Select(choices=enumerate(range(1, parent_column_amount + 1)))
