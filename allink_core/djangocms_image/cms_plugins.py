# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase

from cms.plugin_pool import plugin_pool
from .models import AllinkImagePlugin
from .forms import AllinkImagePluginForm


@plugin_pool.register_plugin
class CMSAllinkImagePlugin(CMSPluginBase):
    model = AllinkImagePlugin
    name = _('Image')
    module = _("allink")
    form = AllinkImagePluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': (
                    'picture',
                    'external_picture',
                )
            }),
            (_('Advanced settings'), {
                'classes': ('collapse',),
                'fields': (
                    'template',
                    'caption_text',
                    'attributes',
                )
            }),
            (_('Link settings'), {
                'classes': ('collapse',),
                'fields': (
                    ('link_url', 'link_page',),
                    ('link_mailto', 'link_phone'),
                    ('link_anchor', 'link_special'),
                    'link_file',
                    'link_target',
                )
            }),
            (_('Wireframe settings'), {
                'classes': ('collapse',),
                'fields': (
                    ('width', 'use_no_cropping'),
                )
            })
        ]

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'djangocms_image/{}/content.html'.format(instance.template)
        return template
