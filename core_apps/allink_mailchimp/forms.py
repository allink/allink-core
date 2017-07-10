# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import get_language, ugettext_lazy as _

from allink_core.core_apps.allink_mailchimp.config import MailChimpConfig
from allink_core.core_apps.allink_mailchimp.helpers import list_members_put, get_status_if_new

from .models import AllinkSignupFormPlugin

config = MailChimpConfig()


class SignupForm(forms.Form):
    email = forms.EmailField(label=_(u'Email'))
    language = forms.CharField(max_length=3, required=False)

    def save(self):
        email = self.cleaned_data['email']
        language = self.cleaned_data['language'] if 'language' in self.cleaned_data else get_language()

        data = {
            'email_address': email,
            'status': 'subscribed',
            'status_if_new': get_status_if_new(),
            'language': language
        }

        if config.merge_vars:
            data = data.update(config.merge_vars)

        list_members_put(data)


class SignupFormAdvanced(forms.Form):
    first_name = forms.CharField(label=_(u'First Name'))
    last_name = forms.CharField(label=_(u'Last Name'))
    email = forms.EmailField(label=_(u'Email'))
    language = forms.CharField(max_length=3, required=False)

    def save(self):
        email = self.cleaned_data['email']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        language = self.cleaned_data['language'] if 'language' in self.cleaned_data else get_language()

        data = {
            'email_address': email,
            'status': 'subscribed',
            'status_if_new': get_status_if_new(),
            'language': language,
            'merge_fields': {
                'FNAME': first_name,
                'LNAME': last_name
            }
        }

        if config.merge_vars:
            data = data.update(config.merge_vars)

        list_members_put(data)


class AllinkSignupFormPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkSignupFormPlugin
        fields = (
            'signup_form',
        )
