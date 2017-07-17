# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from allink_core.core_apps.allink_pdf.models import AllinkPdfPageBreakPlugin
from allink_core.core_apps.allink_pdf.forms import AllinkPdfPageBreakPluginForm


@plugin_pool.register_plugin
class CMSAllinkPageBreakPlugin(CMSPluginBase):
    model = AllinkPdfPageBreakPlugin
    name = _('PDF Page Break')
    module = _('Generic')
    form = AllinkPdfPageBreakPluginForm

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_pdf/content.html'
        return template
