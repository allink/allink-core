# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import AllinkTerms, AllinkTermsPlugin
from .forms import AllinkTermsPluginForm


@plugin_pool.register_plugin
class CMSAllinkTermsPlugin(CMSPluginBase):
    model = AllinkTermsPlugin
    name = _('Terms of Service')
    module = _("allink Apps")
    form = AllinkTermsPluginForm
    render_template = 'allink_terms/plugins/terms.html'

    @classmethod
    def get_render_queryset(cls):
        return cls.model._default_manager.all()

    def render(self, context, instance, placeholder):


      context['instance'] = instance
      context['placeholder'] = placeholder
      context['current_terms'] = AllinkTerms.objects.get_published()

      return context