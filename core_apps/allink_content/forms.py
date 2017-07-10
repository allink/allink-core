# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from allink_core.core.utils import get_additional_choices
from allink_core.core.forms.fields import ColorField
from allink_core.core_apps.allink_content.models import AllinkContentPlugin, AllinkContentColumnPlugin


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
        if get_additional_choices('CONTENT_TITLE_CHOICES'):
            self.fields['title_size'] = forms.CharField(
                label=_(u'Section Title Size'),
                widget=forms.Select(
                    choices=get_additional_choices('CONTENT_TITLE_CHOICES'),
                ),
                initial=settings.CONTENT_TITLE_CHOICES_DEFAULT,
                required=False,
            )
        else:
            self.fields['title_size'] = forms.CharField(widget=forms.HiddenInput(), required=False)

        self.fields['bg_color'] = ColorField(
            label=_(u'Background color'),
            required=False,
        )

        if get_additional_choices('CONTENT_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label=_(u'Predifined variations'),
                choices=get_additional_choices('CONTENT_CSS_CLASSES'),
                required=False,
            )
        if get_additional_choices('CONTENT_ON_SCREEN_EFFECT_CHOICES'):
            self.fields['project_on_screen_effect'] = forms.ChoiceField(
                label=_(u'Predifined on screen Effect'),
                choices=get_additional_choices('CONTENT_ON_SCREEN_EFFECT_CHOICES', blank=True),
                initial='default',
                required=False,
            )

    def clean(self):
        cleaned_data = super(AllinkContentPluginForm, self).clean()
        if self.instance.pk:
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
