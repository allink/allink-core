# -*- coding: utf-8 -*-
from django.utils.translation import get_language
from allink_core.core.views import AllinkBasePluginAjaxCreateView
from .models import DummyAppSignup
from .forms import DummyAppSignupForm
from .cms_plugins import DummyAppSignupPlugin
from .emails import DummyAppSignupConfirmationEmail, DummyAppSignupInternalEmail


class DummyAppSignupView(AllinkBasePluginAjaxCreateView):
    model = DummyAppSignup
    form_class = DummyAppSignupForm
    template_name = 'dummy_app/plugins/signup/content.html'

    success_template_name = 'dummy_app/plugins/signup/success.html'
    plugin_model = DummyAppSignupPlugin

    def form_valid(self, form):
        response = super(DummyAppSignupView, self).form_valid(form)

        DummyAppSignupConfirmationEmail(form=form, plugin=self.plugin_instance, language=get_language()).send_mail()
        DummyAppSignupInternalEmail(form=form, plugin=self.plugin_instance, language=get_language()).send_mail()

        return response
