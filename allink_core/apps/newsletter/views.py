# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.module_loading import import_string
from django.views.generic import FormView

from allink_core.apps.newsletter.forms import SignupForm
from allink_core.core_apps.allink_mailchimp.config import MailChimpConfig

config = MailChimpConfig()


class SignupViewBase(FormView):
    form_class = None
    template_name = None

    def __init__(self, **kwargs):
        super(SignupViewBase, self).__init__(**kwargs)
        if config.signup_form:
            self.form_class = import_string(config.signup_form)

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.render_to_response(self.get_context_data(form=form), status=206)

    def form_valid(self, form, **kwargs):
        context = super(SignupViewBase, self).get_context_data(**kwargs)
        try:
            form.save()
            json_context = {}
            json_context['rendered_content'] = render_to_string('newsletter/confirmation.html', context=context,
                                                                request=self.request)
            return HttpResponse(content=json.dumps(json_context), content_type='application/json', status=200)
        except:
            # sentry is not configured on localhost
            if not settings.RAVEN_CONFIG.get('dsn'):
                raise
            form.add_error(None, _('Something went wrong with your subscription. Please try again later.'))
            return self.render_to_response(self.get_context_data(form=form), status=206)

    def get_context_data(self, **kwargs):
        data = super(SignupViewBase, self).get_context_data(**kwargs)
        data['newsletter_signup_form'] = data.get('form')
        data['placeholder_enabled'] = True
        return data


class SignupView(SignupViewBase):
    form_class = SignupForm
    template_name = 'newsletter/signup_form.html'
