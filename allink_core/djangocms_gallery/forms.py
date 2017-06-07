# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from allink_core.allink_base.utils import get_ratio_choices, get_additional_choices
from allink_core.djangocms_gallery.models import AllinkGalleryPlugin, AllinkGalleryImagePlugin


class AllinkGalleryPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkGalleryPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkGalleryPluginForm, self).__init__(*args, **kwargs)
        self.fields['ratio'] = forms.CharField(
            label=_(u'Ratio'),
            help_text=_(u'This option overrides the default settings for the gallery plugin.'),
            widget=forms.Select(choices=get_ratio_choices()),
            required=False,
        )
        self.fields['template'] = forms.CharField(
            label=_(u'Template'),
            widget=forms.Select(choices=self.instance.get_templates()),
            required=True,
        )
        if get_additional_choices('GALLERY_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                label=_(u'Predifined variations'),
                help_text=_(u'Instructions: Single selection is made by clicking on an option. Multiple selections are achieved by pressing and holding down the Command-key (Mac) or Control-Key (Windows) <strong>and</strong> clicking the options you would like to apply.'),
                choices=get_additional_choices('GALLERY_CSS_CLASSES'),
                required=False,
            )


class AllinkGalleryImagePluginForm(forms.ModelForm):

    class Meta:
        model = AllinkGalleryImagePlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
