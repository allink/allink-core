# -*- coding: utf-8 -*-
from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from djangocms_text_ckeditor.cms_plugins import TextPlugin, Text
from django.conf import settings

from allink_core.core_apps.allink_seo_accordion.models import AllinkSEOAccordionContainerPlugin, AllinkSEOAccordion


@plugin_pool.register_plugin
class CMSAllinkSEOAccordionContainerPlugin(CMSPluginBase):
    model = AllinkSEOAccordionContainerPlugin
    name = 'SEO Accordion Container'
    module = 'Generic'
    allow_children = True
    child_classes = ['CMSAllinkSEOAccordionPlugin']

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'is_seo_faq',
                ),
            }),
        )

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_seo_accordion/content.html'
        return template

    def save_model(self, request, obj, form, change):
        # Create 3 seo accordion entries on plugin creation with text plugin inside
        response = super().save_model(request, obj, form, change)
        if obj.numchild == 0:
            column_amount = 3

            for x in range(column_amount):
                plugin = AllinkSEOAccordion(
                    parent=obj,
                    placeholder=obj.placeholder,
                    language=obj.language,
                    position=CMSPlugin.objects.filter(parent=obj).count(),
                    plugin_type=CMSAllinkSEOAccordionPlugin.__name__
                )
                plugin.title = 'Title {}'.format(x + 1)
                plugin.save()

                child_plugin = Text(
                    parent=plugin,
                    placeholder=plugin.placeholder,
                    language=plugin.language,
                    position=CMSPlugin.objects.filter(parent=plugin).count(),
                    plugin_type=TextPlugin.__name__
                )
                child_plugin.save()
        return response


@plugin_pool.register_plugin
class CMSAllinkSEOAccordionPlugin(CMSPluginBase):
    model = AllinkSEOAccordion
    name = 'SEO Accordion Item'
    module = 'Generic'
    allow_children = True
    child_classes = settings.ALLINK_SEOACCORDION_PLUGIN_CHILD_CLASSES
    text_enabled = False

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'title',
                ),
            }),
        )

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_seo_accordion/item.html'
        return template
