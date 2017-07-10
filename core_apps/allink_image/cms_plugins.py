# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from webpack_loader.utils import get_files

from cms.plugin_pool import plugin_pool

from allink_core.core.utils import get_project_color_choices
from allink_core.core_apps.allink_image.models import AllinkImagePlugin
from allink_core.core_apps.allink_image.forms import AllinkImagePluginForm


@plugin_pool.register_plugin
class CMSAllinkImagePlugin(CMSPluginBase):
    model = AllinkImagePlugin
    name = _('Image')
    module = _("allink")
    form = AllinkImagePluginForm

    class Media:
        js = (
            get_files('djangocms_custom_admin')[0]['publicPath'],
        )
        css = {
            'all': (
                get_files('djangocms_custom_admin')[1]['publicPath'],

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
                    'attributes',
                ]
            }),
            (_('Link settings'), {
                'classes': ('collapse',),
                'fields': (
                    ('link_url', 'internal_link',),
                    ('link_mailto', 'link_phone'),
                    ('link_anchor', 'link_special'),
                    'link_file',
                    'link_target',
                )
            }),
        ]

        if get_project_color_choices():
            fieldsets[0][1].get('fields').append('bg_color')
        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_image/content.html'
        return template
