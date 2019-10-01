# -*- coding: utf-8 -*-
from django import forms

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from allink_core.core_apps.allink_terms.models import AllinkTerms
from allink_core.core_apps.allink_terms.models import AllinkTermsPlugin


class AllinkTermsPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkTermsPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')


@plugin_pool.register_plugin
class CMSAllinkTermsPlugin(CMSPluginBase):
    model = AllinkTermsPlugin
    name = 'Terms of Service'
    module = 'allink modules'
    form = AllinkTermsPluginForm
    render_template = 'allink_terms/plugins/terms.html'

    def render(self, context, instance, placeholder):

        context['instance'] = instance
        context['placeholder'] = placeholder
        context['current_terms'] = AllinkTerms.objects.get_published()

        return context
