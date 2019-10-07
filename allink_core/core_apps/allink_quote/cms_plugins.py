from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import QuotePlugin


@plugin_pool.register_plugin
class CMSQuotePlugin(CMSPluginBase):
    name = _('Quote')
    module = _('allink modules')
    render_template = 'allink_quote/content.html'
    model = QuotePlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['placeholder'] = placeholder
        return context
