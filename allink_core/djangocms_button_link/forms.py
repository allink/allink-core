# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import Media, TextInput
from djangocms_attributes_field.widgets import AttributesWidget
from django.utils.translation import ugettext_lazy as _

from allink_core.djangocms_button_link.models import AllinkButtonLinkContainerPlugin, AllinkButtonLinkPlugin
from allink_core.allink_base.models.model_fields import choices_from_sitemaps


class AllinkButtonLinkContainerPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkButtonLinkContainerPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')


class AllinkButtonLinkPluginForm(forms.ModelForm):

    link_internal = forms.ChoiceField(choices=(), required=False)

    class Meta:
        model = AllinkButtonLinkPlugin
        exclude = (
            'page', 'position', 'placeholder', 'language', 'plugin_type',
        )
        # When used inside djangocms-text-ckeditor
        # this causes the label field to be prefilled with the selected text.
        widgets = {
            'label': TextInput(attrs={'class': 'js-ckeditor-use-selected-text'}),
        }

    def __init__(self, *args, **kwargs):
        super(AllinkButtonLinkPluginForm, self).__init__(*args, **kwargs)
        self.fields['link_attributes'].widget = AttributesWidget()
        self.fields['link_special'] = forms.CharField(
            label=_(u'Special Links'),
            widget=forms.Select(choices=self.instance.get_link_special_choices()),
            required=False,
        )
        self.fields['link_internal'].choices = choices_from_sitemaps()

    def _get_media(self):
        """
        Provide a description of all media required to render the widgets on this form
        """
        media = Media()
        for field in self.fields.values():
            media = media + field.widget.media
        media._js = ['cms/js/libs/jquery.min.js'] + media._js
        return media
    media = property(_get_media)
