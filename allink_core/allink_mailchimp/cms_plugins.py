# # -*- coding: utf-8 -*-
#
# from django.utils.translation import ugettext_lazy as _
# from django.utils.module_loading import import_by_path
#
# from cmsplugin_form_handler.cms_plugins import FormPluginBase
# from cms.plugin_pool import plugin_pool
#
# from .config import MailChimpConfig
# config = MailChimpConfig()
#
# from .models import AllinkSignupFormPlugin
# from .forms import SignupForm
#
#
# @plugin_pool.register_plugin
# class CMSAllinkSignupFormPlugin(FormPluginBase):
#     model = AllinkSignupFormPlugin
#     name = _('Signup Form')
#     module = _("allink")
#     render_template = "allink_mailchimp/plugins/signup_form.html"
#     allow_children = False
#
#     form_class = SignupForm
#     success_url = '/success/'
#
#     class Media:
#         js = ('build/djangocms_custom_admin_scripts.js', )
#         css = {
#              'all': ('build/djangocms_custom_admin_style.css', )
#         }
#
#     def get_form(self, request, instance):
#         if config.signup_form:
#             return import_by_path(config.signup_form)
#         else:
#             return self.form_class
#
#
#     def render(self, context, instance, placeholder):
#         context = super(CMSAllinkSignupFormPlugin, self).render(context, instance, placeholder)
#         return context
#
