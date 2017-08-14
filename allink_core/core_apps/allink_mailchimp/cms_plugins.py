# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from webpack_loader.utils import get_files

from .config import MailChimpConfig
from .models import AllinkSignupFormPlugin

config = MailChimpConfig()


class AllinkSignupFormPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkSignupFormPlugin
        fields = (
            'signup_form',
        )


@plugin_pool.register_plugin
class CMSAllinkSignupFormPlugin(CMSPluginBase):
    model = AllinkSignupFormPlugin
    name = _(u'Signup Form')
    module = _('allink forms')
    render_template = "allink_mailchimp/plugins/signup_form.html"
    allow_children = False

    form_class = AllinkSignupFormPluginForm
    success_url = '/success/'

    class Media:
        js = (get_files('djangocms_custom_admin')[0]['publicPath'], )
        css = {
            'all': (get_files('djangocms_custom_admin')[1]['publicPath'], )
        }

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
