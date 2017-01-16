# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import get_language, ugettext_lazy as _

from cmsplugin_form_handler.forms import FormPluginFormMixin
from .config import MailChimpConfig
from .helpers import subscribe_member_to_list, get_status_if_new

config = MailChimpConfig()


class SignupForm(FormPluginFormMixin, forms.Form):
    email = forms.EmailField(label=_(u'E-Mail'))
    language = forms.CharField(max_length=3, required=False)

    def save(self):
        email = self.cleaned_data['email']

        # print 'LANGUAGE:: {}'.format(self.cleaned_data['language'])
        print 'EMAIL:: {}'.format(self.cleaned_data['language'])
        language = self.cleaned_data['language'] if 'language' in self.cleaned_data else get_language()

        merge_vars = {}
        merge_vars.update(config.additional_fields)  # adding extra fields with default value

        data = {
            'email_address': email,
            'status': 'subscribed',
            'status_if_new': get_status_if_new(),
            'language': language,
            'merge_fields': merge_vars
        }

        subscribe_member_to_list(data)
