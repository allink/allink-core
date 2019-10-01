# -*- coding: utf-8 -*-
from django import forms
from django.contrib.postgres.forms import SplitArrayField
from cms.plugin_base import CMSPluginBase

from cms.plugin_pool import plugin_pool
from webpack_loader.utils import get_files

from allink_core.core.utils import get_additional_choices
from allink_core.core.loading import get_model
from allink_core.core.admin.mixins import AllinkMediaAdminMixin

ContactRequestPlugin = get_model('contact', 'ContactRequestPlugin')


class ContactRequestFormPluginForm(AllinkMediaAdminMixin, forms.ModelForm):
    internal_email_addresses = SplitArrayField(forms.EmailField(required=False), size=3)

    class Meta:
        model = ContactRequestPlugin
        fields = ('send_internal_mail', 'internal_email_addresses', 'from_email_address', 'send_external_mail',
                  'thank_you_text', 'label_layout', 'project_css_classes')

    def __init__(self, *args, **kwargs):
        super(ContactRequestFormPluginForm, self).__init__(*args, **kwargs)
        if get_additional_choices('FORM_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label='Predefined variations',
                choices=get_additional_choices('FORM_CSS_CLASSES'),
                required=False,
            )
        else:
            self.fields['project_css_classes'].widget = forms.widgets.HiddenInput()


@plugin_pool.register_plugin
class CMSAllinkContactRequestPlugin(CMSPluginBase):
    model = ContactRequestPlugin
    name = 'Contact Form'
    module = 'allink forms'
    form = ContactRequestFormPluginForm

    def get_render_template(self, context, instance, placeholder):
        template = 'contact/content.html'
        return template
