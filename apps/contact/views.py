# -*- coding: utf-8 -*-
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
        if plugin_id:
            self.plugin = ContactRequestPlugin.objects.get(id=plugin_id)
        return super(ContactRequestView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        response = super(ContactRequestView, self).form_valid(form)
        self.send_mail()
        return response

    def send_mail(self):
        if not self.plugin or self.plugin.send_internal_mail:
            send_request_email(self.get_form(), self.plugin)
        if not self.plugin or self.plugin.send_external_mail:
            send_request_confirmation_email(self.get_form(), self.plugin)
