# -*- coding: utf-8 -*-
from django import forms
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from webpack_loader.utils import get_files

from .config import MailChimpConfig
from .models import AllinkSignupFormPlugin
from allink_core.core.admin.mixins import AllinkMediaAdminMixin

config = MailChimpConfig()


class AllinkSignupFormPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkSignupFormPlugin
        fields = (
            'signup_form',
        )


@plugin_pool.register_plugin
class CMSAllinkSignupFormPlugin(AllinkMediaAdminMixin, CMSPluginBase):
    model = AllinkSignupFormPlugin
    name = 'Signup Form'
    module = 'allink forms'
    render_template = "allink_mailchimp/plugins/signup_form.html"
    allow_children = False

    form_class = AllinkSignupFormPluginForm
    success_url = '/success/'

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(CMSAllinkSignupFormPlugin, self).get_fieldsets(request, obj)
        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        if instance and instance.signup_form == 'advanced':
            template = 'allink_mailchimp/plugins/signup_form_advanced.html'.format(instance.signup_form)
        else:
            template = self.render_template
        return template

    def render(self, context, instance, placeholder):
        context = super(CMSAllinkSignupFormPlugin, self).render(context, instance, placeholder)
        return context
