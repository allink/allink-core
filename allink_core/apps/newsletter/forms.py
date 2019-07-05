# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import get_language, ugettext_lazy as _

from allink_core.core_apps.allink_mailchimp.config import MailChimpConfig
from allink_core.core_apps.allink_mailchimp.helpers import list_members_put, get_status_if_new
from allink_core.core.models.choices import SALUTATION_CHOICES, MR

config = MailChimpConfig()


class SignupForm(forms.Form):
    salutation = forms.IntegerField(
        label=_('Salutation'),
        widget=forms.RadioSelect(choices=SALUTATION_CHOICES),
        initial=MR
    )
    first_name = forms.CharField(
        label=_('First Name')
    )
    last_name = forms.CharField(
        label=_('Last Name')
    )
    email = forms.EmailField(
        label=_('Email')
    )
    language = forms.CharField(
        max_length=3, required=False
    )
    # gdpr permission options
    permission_direct_mail = forms.BooleanField(
        label=_('Email'),
        required=False
    )
    permission_personalised_online_advertising = forms.BooleanField(
        label=_('Personalised online advertising'),
        required=False
    )

    def save(self):
        salutation = 'Herr' if self.cleaned_data['salutation'] == 1 else 'Frau'
        email = self.cleaned_data['email']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        language = self.cleaned_data['language'] if 'language' in self.cleaned_data else get_language()
        permission_direct_mail = self.cleaned_data['permission_direct_mail']
        permission_personalised_online_advertising = self.cleaned_data['permission_personalised_online_advertising']

        data = {
            'email_address': email,
            'status': 'subscribed',
            'status_if_new': get_status_if_new(),
            'language': language,
            'merge_fields': {
                'GENDER': salutation,
                'FNAME': first_name,
                'LNAME': last_name,
                'GDPR_EMAIL': 'Yes' if permission_direct_mail else 'No',
                'GDPR_ADS': 'Yes' if permission_personalised_online_advertising else 'No',
            }
        }

        if config.merge_vars:
            data = data.update(config.merge_vars)

        list_members_put(data)
