from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import AllinkListMulticolPlugin


@plugin_pool.register_plugin
class CMSAllinkListMulticolPlugin(CMSPluginBase):
    name = 'List Multicol'
    module = 'Generic'
    render_template = 'allink_list_multicol/content.html'
    model = AllinkListMulticolPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['placeholder'] = placeholder
        return context
