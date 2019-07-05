# -*- coding: utf-8 -*-
from django.views.generic import CreateView
from allink_core.core.loading import get_model, get_class
from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView, AllinkBaseCreateView
from allink_core.core_apps.allink_mandrill.config import MandrillConfig


Events = get_model('events', 'Events')
EventsAppContentPlugin = get_model('events', 'EventsAppContentPlugin')
EventsRegistration = get_model('events', 'EventsRegistration')
EventsRegistrationForm = get_class('events.forms', 'EventsRegistrationForm')
send_registration_confirmation_email = get_class('events.email', 'send_registration_confirmation_email')
send_registration_email = get_class('events.email', 'send_registration_email')


config = MandrillConfig()


class EventsPluginLoadMore(AllinkBasePluginLoadMoreView):
    model = Events
    plugin_model = EventsAppContentPlugin


class EventsDetail(AllinkBaseDetailView):
    model = Events


class EventsRegistrationView(AllinkBaseCreateView):
    model = EventsRegistration
    form_class = EventsRegistrationForm
    template_name = 'events/forms/registration.html'

    def get_context_data(self, **kwargs):
        context = CreateView.get_context_data(self)
        context.update({
            'slug': self.kwargs.get('slug', None),
            'event_title': self.item.title
        })
        return context

    def get_initial(self):
        self.item = Events.objects.get(translations__slug=self.kwargs.get('slug', None))
        initial = super(EventsRegistrationView, self).get_initial()
        initial = initial.copy()
        initial['event'] = self.item
        # initial['terms'] = AllinkTerms.objects.get_published()  # for reference
        return initial

    def form_valid(self, form):
        response = super(EventsRegistrationView, self).form_valid(form)
        self.send_mail()
        return response

    def send_mail(self):
        send_registration_email(self.get_form(), self.item)
        send_registration_confirmation_email(self.get_form(), self.item)
