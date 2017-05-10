# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase

from cms.plugin_pool import plugin_pool
from allink_core.djangocms_image.models import AllinkImagePlugin
from allink_core.djangocms_image.forms import AllinkImagePluginForm
from allink_core.allink_base.utils.utils import get_project_color_choices


@plugin_pool.register_plugin
class CMSAllinkImagePlugin(CMSPluginBase):
    model = AllinkImagePlugin
    name = _('Image')
    module = _("allink")
    form = AllinkImagePluginForm

    class Media:
        js = (
            'build/djangocms_custom_admin_scripts.js',
        )
        css = {
            'all': (
                'build/djangocms_custom_admin_style.css',

            )
        }

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': [
                    'picture',
                    'ratio',
                    'project_css_classes',
                    'icon_enabled',
                    'bg_enabled',
                ]
            }),
            (_('Additional settings'), {
                'classes': ('collapse',),
                'fields': [
                    'caption_text',
                    'external_picture',
                    'template',
                    'attributes',
                ]
            }),
            (_('Link settings'), {
                'classes': ('collapse',),
                'fields': (
                    ('link_url', 'link_internal',),
                    ('link_mailto', 'link_phone'),
                    ('link_anchor', 'link_special'),
                    'link_file',
                    'link_target',
                )
            }),
            # Replaced with our "original" option
            # (_('Wireframe settings'), {
            #     'classes': ('collapse',),
            #     'fields': (
            #         ('width', 'use_no_cropping'),
            #     )
            # })
        ]

        if get_project_color_choices():
            fieldsets[0][1]['fields'].append('bg_color')

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'djangocms_image/{}/content.html'.format(instance.template)
        return template
