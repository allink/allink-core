# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.utils.module_loading import import_by_path

from cms.plugin_base import CMSPluginBase
from cmsplugin_form_handler.cms_plugins import FormPluginBase
from cms.plugin_pool import plugin_pool
from webpack_loader.utils import get_files

from .config import MailChimpConfig
config = MailChimpConfig()

from .models import AllinkSignupFormPlugin
from .forms import AllinkSignupFormPluginForm


@plugin_pool.register_plugin
class CMSAllinkSignupFormPlugin(CMSPluginBase):
    model = AllinkSignupFormPlugin
    name = _('Signup Form')
    module = _("allink")
    render_template = "allink_mailchimp/plugins/signup_form.html"
    allow_children = False

    form_class = AllinkSignupFormPluginForm
    success_url = '/success/'

    class Media:
        js = (get_files('djangocms_custom_admin_scripts')[0]['publicPath'], )
        css = {
             'all': (get_files('djangocms_custom_admin_style')[0]['publicPath'], )
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
