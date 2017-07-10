# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.forms import SplitArrayField
from cms.plugin_base import CMSPluginBase

from cms.plugin_pool import plugin_pool
from webpack_loader.utils import get_files

from allink_core.core.utils import get_additional_choices
from allink_core.core.loading import get_model

ContactRequestPlugin = get_model('contact', 'ContactRequestPlugin')


class ContactRequestFormPluginForm(forms.ModelForm):
    internal_email_adresses = SplitArrayField(forms.EmailField(required=False), size=3)

    class Media:
        js = (get_files('djangocms_custom_admin')[0]['publicPath'], )
        css = {
            'all': (get_files('djangocms_custom_admin')[1]['publicPath'], )
        }

    class Meta:
        model = ContactRequestPlugin
        fields = ('send_internal_mail', 'internal_email_adresses', 'from_email_address', 'send_external_mail', 'thank_you_text', 'label_layout', 'project_css_classes')

    def __init__(self, *args, **kwargs):
        super(ContactRequestFormPluginForm, self).__init__(*args, **kwargs)
        if get_additional_choices('FORM_CSS_CLASSES'):
            self.fields['project_css_classes'] = forms.MultipleChoiceField(
                widget=forms.CheckboxSelectMultiple(),
                label=_(u'Predifined variations'),
                choices=get_additional_choices('FORM_CSS_CLASSES'),
                required=False,
            )
        else:
            self.fields['project_css_classes'].widget = forms.widgets.HiddenInput()


@plugin_pool.register_plugin
class CMSAllinkContactRequestPlugin(CMSPluginBase):
    model = ContactRequestPlugin
    name = _('ContactRequest')
    module = _("allink")
    form = ContactRequestFormPluginForm

    def get_render_template(self, context, instance, placeholder):
        template = 'contact/content.html'
        return template
