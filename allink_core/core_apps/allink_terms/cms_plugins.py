# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from allink_core.core_apps.allink_terms.models import AllinkTerms, AllinkTermsPlugin
from allink_core.core_apps.allink_terms.forms import AllinkTermsPluginForm


@plugin_pool.register_plugin
class CMSAllinkTermsPlugin(CMSPluginBase):
    model = AllinkTermsPlugin
    name = _('Terms of Service')
    module = _('allink modules')
    form = AllinkTermsPluginForm
    render_template = 'allink_terms/plugins/terms.html'

    def render(self, context, instance, placeholder):

        context['instance'] = instance
        context['placeholder'] = placeholder
        context['current_terms'] = AllinkTerms.objects.get_published()

        return context
