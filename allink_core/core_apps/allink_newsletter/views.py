from raven import Client

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from allink_core.core.views import AllinkBasePluginAjaxCreateView
from allink_core.core_apps.allink_newsletter.forms import NewsletterSignupForm
from allink_core.core_apps.allink_newsletter.models import NewsletterSignupLog, NewsletterSignupPlugin
from allink_core.core_apps.allink_newsletter.base import AllinkMailchimp, MailchimpException


class NewsletterSignupView(AllinkBasePluginAjaxCreateView):
    model = NewsletterSignupLog
    form_class = NewsletterSignupForm
    template_name = 'allink_newsletter/content.html'

    plugin_model = NewsletterSignupPlugin
    success_template_name = 'allink_newsletter/success.html'

    def form_valid(self, form):
        response = super(NewsletterSignupView, self).form_valid(form)
        obj = AllinkMailchimp()
        try:
            obj.subscribe_to_audience(*self.get_fields_from_form(form),
                                      audience_id=self.get_audience_id(),
                                      mailchimp_api_key=settings.MAILCHIMP_API_KEY,
                                      double_opt_in_status=self.get_double_opt_in_status(),
                                      marketing_permission_email_id=self.get_marketing_permission_email_id(),
                                      marketing_permission_personalised_marketing_id=self.get_marketing_permission_personalised_marketing_id(),
                                      marketing_permission_direct_mailing_id=self.get_marketing_permission_direct_mailing_id(),
                                      mailchimp_datacenter=self.get_mailchimp_datacenter()
                                      )
        except MailchimpException:
            client = Client(settings.RAVEN_CONFIG.get('dsn'))
            client.captureException()

            form.add_error(None, _('Something went wrong on our end we are sorry for that'))
            response = self.form_invalid(form)

        return response

    def get_fields_from_form(self, form):
        salutation = form.instance.get_salutation_display()
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        allows_gdpr_email = form.cleaned_data['allows_gdpr_email']
        allows_gdpr_personalised_marketing = form.cleaned_data['allows_gdpr_personalised_marketing']
        allows_gdpr_direct_mailing = form.cleaned_data['allows_gdpr_direct_mailing']
        return salutation, first_name, last_name, email, allows_gdpr_email, allows_gdpr_personalised_marketing, \
               allows_gdpr_direct_mailing

    def get_double_opt_in_status(self):
        double_opt_in_status = 'pending' if self.plugin_instance.double_opt_in_enabled else 'subscribed'
        return double_opt_in_status

    def get_audience_id(self):
        audience_id = self.plugin_instance.audience_id
        return audience_id

    def get_marketing_permission_email_id(self):
        return self.plugin_instance.marketing_permission_email_id

    def get_marketing_permission_personalised_marketing_id(self):
        return self.plugin_instance.marketing_permission_personalised_marketing_id

    def get_marketing_permission_direct_mailing_id(self):
        return self.plugin_instance.marketing_permission_direct_mailing_id

    def get_mailchimp_datacenter(self):
        return settings.MAILCHIMP_DATACENTER
