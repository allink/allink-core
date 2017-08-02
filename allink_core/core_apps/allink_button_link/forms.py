# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import Media, TextInput
from djangocms_attributes_field.widgets import AttributesWidget
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.forms import SplitArrayField

from allink_core.core_apps.allink_button_link.models import AllinkButtonLinkContainerPlugin, AllinkButtonLinkPlugin
from allink_core.core.utils import get_additional_choices
from allink_core.core.forms.fields import SelectLinkField
from allink_core.core.forms.mixins import AllinkInternalLinkFieldMixin


class AllinkButtonLinkContainerPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkButtonLinkContainerPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkButtonLinkContainerPluginForm, self).__init__(*args, **kwargs)
        if get_additional_choices('BUTTON_LINK_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label=_(u'Predifined variations'),
                choices=get_additional_choices('BUTTON_LINK_CSS_CLASSES'),
                required=False,
            )


class AllinkButtonLinkPluginForm(AllinkInternalLinkFieldMixin, forms.ModelForm):

    internal_link = SelectLinkField(label=_('Link Internal'), required=False)
    internal_email_addresses = SplitArrayField(forms.EmailField(required=False), size=3, required=False)

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
            help_text=_(u'Important: In case the selected option is a <strong>form</strong>, make sure to select <strong>Lightbox (Forms)</strong> from the <strong>link target</strong> options for best user experience.'),
        )

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


    def clean(self):
        from django.core.exceptions import ValidationError
        # If special_link is a form which sends emails all the additional fields have to be supplied
        if ':request' in self.cleaned_data.get('link_special') and \
            (self.cleaned_data.get('send_internal_mail') == True
             and not self.cleaned_data.get('internal_email_addresses')[0]
             and not self.cleaned_data.get('internal_email_addresses')[1]
             and not self.cleaned_data.get('internal_email_addresses')[2]):
            self.add_error('internal_email_addresses', ValidationError(_(u'Please supply at least one E-Mail Address.')))
        if ':request' in self.cleaned_data.get('link_special') and (self.cleaned_data.get('send_external_mail') == True and not self.cleaned_data.get('from_email_address')):
            self.add_error('from_email_address', ValidationError(_(u'Please supply an E-Mail Address.')))
        return self.cleaned_data
