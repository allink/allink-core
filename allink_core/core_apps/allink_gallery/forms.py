# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags

from allink_core.core.utils import get_ratio_choices, get_additional_choices
from allink_core.core_apps.allink_gallery.models import AllinkGalleryPlugin, AllinkGalleryImagePlugin
from allink_core.core.loading import get_model

Config = get_model('config', 'Config')


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
                widget=forms.CheckboxSelectMultiple(),
                label=_(u'Predifined variations'),
                choices=get_additional_choices('GALLERY_CSS_CLASSES'),
                required=False,
            )


class AllinkGalleryImagePluginForm(forms.ModelForm):

    class Meta:
        model = AllinkGalleryImagePlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def clean(self):
        cleaned_data = super(AllinkGalleryImagePluginForm, self).clean()
        form_data = self.cleaned_data
        text_length = len(strip_tags(form_data['text']))
        gallery_plugin_caption_text_max_length = getattr(Config.get_solo(), 'gallery_plugin_caption_text_max_length')

        if gallery_plugin_caption_text_max_length and text_length > gallery_plugin_caption_text_max_length:
            self.add_error('text', _(u'There are only {} characters allowed in text field. Currently there are {} characters.').format(gallery_plugin_caption_text_max_length, text_length))

        return cleaned_data
