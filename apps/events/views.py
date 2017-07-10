# -*- coding: utf-8 -*-

from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from allink_core.core.loading import get_model, get_class
from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView, AllinkBaseCreateView
from allink_core.core_apps.allink_mandrill.config import MandrillConfig
from allink_core.core_apps.allink_terms.models import AllinkTerms


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
    template_name = 'events/events_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if not self.object.is_published():
            raise Http404(_('{} is not published.'.format(self.model.get_verbose_name())))
        else:
            return self.render_to_response(context)


class EventsRegistrationView(AllinkBaseCreateView):
    model = EventsRegistration
    form_class = EventsRegistrationForm
    template_name = 'events/forms/registration.html'

    def get_context_data(self, **kwargs):
        context = super(AllinkBaseCreateView, self).get_context_data(**kwargs)
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
        initial['terms'] = AllinkTerms.objects.get_published()  # for reference
        return initial

    def form_valid(self, form):
        response = super(EventsRegistrationView, self).form_valid(form)
        self.send_mail()
        return response

    def send_mail(self):
        send_registration_email(self.get_form(), self.item)
        send_registration_confirmation_email(self.get_form(), self.item)

    def get_confirmation_template(self):
        template = '{}/forms/confirmation.html'.format(self.item._meta.model_name)
        try:
            get_template(template)
        except TemplateDoesNotExist:
            template = 'partials/forms/confirmation.html'
        return template
