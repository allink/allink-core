# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from allink_core.core_apps.allink_mandrill.base import AllinkMandrillFormPluginEmail


class DummyAppSignupConfirmationEmail(AllinkMandrillFormPluginEmail):
    template_name = 'some_client_dummy_app_signup_confirmation'
    google_analytics_campaign = template_name

    def fetch_to_email_addresses(self):
        return [
            self.create_email_to_entry(
                self.form.data.get('email'),
                ''.format(self.form.fields.get('last_name'), self.form.fields.get('first_name'))
            ),
        ]


class DummyAppSignupInternalEmail(AllinkMandrillFormPluginEmail):
    template_name = 'some_client_dummy_app_signup_internal'
    translated = False

    def build_subject(self):
        return _('New inquiry')

    def fetch_to_email_addresses(self):
        return [self.create_email_to_entry(email, self.config.get_default_from_name())
                for email in self.plugin.internal_recipients]
