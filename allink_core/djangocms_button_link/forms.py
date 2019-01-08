# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import Media, TextInput
from djangocms_attributes_field.widgets import AttributesWidget
from django.utils.translation import ugettext_lazy as _

from allink_core.djangocms_button_link.models import AllinkButtonLinkContainerPlugin, AllinkButtonLinkPlugin
from allink_core.allink_base.utils import get_additional_choices, get_ratio_choices
from allink_core.allink_base.models.choices import BLANK_CHOICE, NEW_WINDOW, SOFTPAGE_LARGE, SOFTPAGE_SMALL, FORM_MODAL, IMAGE_MODAL
from allink_core.allink_base.forms.fields import SelectLinkField
from allink_core.allink_base.forms.mixins import AllinkInternalLinkFieldMixin


class AllinkButtonLinkContainerPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkButtonLinkContainerPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')

    def __init__(self, *args, **kwargs):
        super(AllinkButtonLinkContainerPluginForm, self).__init__(*args, **kwargs)
        if get_additional_choices('BUTTON_LINK_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                label=_(u'Predifined variations'),
                help_text=_(u'Instructions: Single selection is made by clicking on an option. Multiple selections are achieved by pressing and holding down the Command-key (Mac) or Control-Key (Windows) <strong>and</strong> clicking the options you would like to apply.'),
                choices=get_additional_choices('BUTTON_LINK_CSS_CLASSES'),
                required=False,
            )
        self.fields['ratio'] = forms.CharField(
            label=_(u'Ratio'),
            help_text=_(u'This option overrides the default ratio setting for embeded videos.'),
            widget=forms.Select(choices=get_ratio_choices()),
            required=False,
        )


class AllinkButtonLinkPluginForm(AllinkInternalLinkFieldMixin, forms.ModelForm):

    LINK_TARGET_REDUCED = (
        (NEW_WINDOW, _(u'New window')),
        (SOFTPAGE_LARGE, _(u'Softpage large')),
        (SOFTPAGE_SMALL, _(u'Softpage small')),
    )

    link_target_reduced = forms.ChoiceField(label=_('Link Target'), required=False, choices=BLANK_CHOICE+LINK_TARGET_REDUCED)
    internal_link = SelectLinkField(label=_('Link Internal'), required=False)

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
        self.fields['ratio'] = forms.CharField(
            label=_(u'Ratio'),
            help_text=_(u'This option overrides the default ratio setting for embeded videos.'),
            widget=forms.Select(choices=get_ratio_choices()),
            required=False,
        )

        self.initial['link_target_reduced'] = self.instance.link_target

    def clean(self):
        cleaned_data = super(AllinkButtonLinkPluginForm, self).clean()

        template = cleaned_data.get("template")

        if template == AllinkButtonLinkPlugin.DEFAULT_LINK:
            cleaned_data['link_target'] = cleaned_data.get('link_target_reduced') if cleaned_data.get('link_target_reduced') else None
        elif template == AllinkButtonLinkPlugin.FORM_LINK:
            cleaned_data['link_target'] = FORM_MODAL
        elif template == AllinkButtonLinkPlugin.FILE_LINK:
            cleaned_data['link_target'] = NEW_WINDOW
        elif template == AllinkButtonLinkPlugin.IMAGE_LINK \
            or template == AllinkButtonLinkPlugin.VIDEO_EMBEDDED_LINK:
            cleaned_data['link_target'] = IMAGE_MODAL

        #  always open external_links in new tab
        if cleaned_data['link_url']:
            cleaned_data['link_target'] = NEW_WINDOW

        return cleaned_data

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
