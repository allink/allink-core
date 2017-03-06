# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.module_loading import import_by_path
from django.views.generic import FormView

from .forms import SignupForm, SignupFormAdvanced
from .config import MailChimpConfig


config = MailChimpConfig()

class SignupViewBase(FormView):
    form_class = None
    template_name = None

    def __init__(self, **kwargs):
        super(SignupViewBase, self).__init__(**kwargs)
        if config.signup_form:
            self.form_class = import_by_path(config.signup_form)

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
            html = render_to_string('allink_mailchimp/confirmation.html', context)
            return HttpResponse(html)
        except:
            # sentry is not configured on localhost
            if not settings.RAVEN_CONFIG.get('dns'):
                raise
            form.add_error(None, _(u'Something went wrong with your subscription. Please try again later.'))
            return self.render_to_response(self.get_context_data(form=form), status=206)

    def get_context_data(self, **kwargs):
        data = super(SignupViewBase, self).get_context_data(**kwargs)
        data['mailchimp_signup_form'] = data.get('form')
        return data


class SignupView(SignupViewBase):
    form_class = SignupForm
    template_name = 'allink_mailchimp/signup_form.html'


class SignupViewAdvanced(SignupViewBase):
    form_class = SignupFormAdvanced
    template_name = 'allink_mailchimp/signup_form_advanced.html'
