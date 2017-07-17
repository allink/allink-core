# -*- coding: utf-8 -*-
from cms.models.pluginmodel import CMSPlugin
from allink_core.core.loading import get_class, get_model
from allink_core.core.views import AllinkBaseCreateView
from allink_core.core_apps.allink_mandrill.config import MandrillConfig


ContactRequest = get_model('contact', 'ContactRequest')
ContactRequestPlugin = get_model('contact', 'ContactRequestPlugin')
ContactRequestForm = get_class('contact.forms', 'ContactRequestForm')
send_request_confirmation_email = get_class('contact.email', 'send_request_confirmation_email')
send_request_email = get_class('contact.email', 'send_request_email')

config = MandrillConfig()


class ContactRequestView(AllinkBaseCreateView):
    model = ContactRequest
    form_class = ContactRequestForm
    template_name = 'contact/forms/request.html'
    plugin = None

    def dispatch(self, *args, **kwargs):
        plugin_id = self.kwargs.pop('plugin_id', None)
        self.plugin = CMSPlugin.objects.get(id=plugin_id).get_plugin_instance()[0]
        return super(ContactRequestView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        response = super(ContactRequestView, self).form_valid(form)
        self.send_mail()
        return response

    def send_mail(self):
        if self.plugin.send_internal_mail:
            send_request_email(self.get_form(), self.plugin)
        if self.plugin.send_external_mail:
            send_request_confirmation_email(self.get_form(), self.plugin)
