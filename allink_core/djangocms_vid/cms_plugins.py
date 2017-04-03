# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase

from cms.plugin_pool import plugin_pool
from .models import AllinkVidPlugin
from .forms import AllinkVidPluginForm


@plugin_pool.register_plugin
class CMSAllinkVidPlugin(CMSPluginBase):
    model = AllinkVidPlugin
    name = _('Video')
    module = _("allink")
    form = AllinkVidPluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': (
                    'label',
                    'poster',
                    'embed_link',
                    'ratio',
                    'template',
                )
            }),
            (_('Advanced settings'), {
                'classes': ('collapse',),
                'fields': (
                    'attributes',
                )
            }),
        ]

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'djangocms_vid/{}/content.html'.format(instance.template)
        return template
