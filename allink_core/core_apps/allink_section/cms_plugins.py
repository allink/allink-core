# -*- coding: utf-8 -*-
from cms.plugin_pool import plugin_pool

from allink_core.core.cms_plugins import CMSAllinkBaseSectionPlugin
from .models import AllinkSectionPlugin


@plugin_pool.register_plugin
class CMSAllinkSectionPlugin(CMSAllinkBaseSectionPlugin):
    model = AllinkSectionPlugin
    name = 'Section'
    # child_classes = ['CMSAllinkTeaserPlugin']
    render_template = 'allink_section/content.html'

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            ('Spacings', {
                'fields': [
                    'project_css_spacings_top_bottom',
                    'project_css_spacings_top',
                    'project_css_spacings_bottom',
                ]
            }),
            ('Section Options', {
                'classes': ('collapse',),
                'fields': [
                    'title',
                    'columns',
                    'column_order',
                    'project_css_classes',
                    'anchor',
                ]
            }),
        )
        return fieldsets
