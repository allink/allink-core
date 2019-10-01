# -*- coding: utf-8 -*-
from django import forms

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from allink_core.core_apps.allink_pdf.models import AllinkPdfPageBreakPlugin


class AllinkPdfPageBreakPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkPdfPageBreakPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')


@plugin_pool.register_plugin
class CMSAllinkPageBreakPlugin(CMSPluginBase):
    model = AllinkPdfPageBreakPlugin
    name = 'PDF Page Break'
    module = 'Generic'
    form = AllinkPdfPageBreakPluginForm

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_pdf/content.html'
        return template
