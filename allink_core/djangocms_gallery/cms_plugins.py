# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from allink_core.djangocms_gallery.models import AllinkGalleryPlugin, AllinkGalleryImagePlugin
from allink_core.djangocms_gallery.forms import AllinkGalleryPluginForm, AllinkGalleryImagePluginForm


@plugin_pool.register_plugin
class CMSAllinkGalleryPlugin(CMSPluginBase):
    model = AllinkGalleryPlugin
    name = _('Gallery')
    module = _("allink")
    allow_children = True
    child_classes = ['CMSAllinkGalleryImagePlugin']
    form = AllinkGalleryPluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'title',
                    'title_size',
                    'template',
                    'ratio',
                ),
            }),
        )

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'djangocms_gallery/{}/content.html'.format(instance.template)
        return template


@plugin_pool.register_plugin
class CMSAllinkGalleryImagePlugin(CMSPluginBase):
    model = AllinkGalleryImagePlugin
    name = _('Image')
    module = _("allink")
    allow_children = False
    form = AllinkGalleryImagePluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'title',
                    'image',
                    'text',
                ),
            }),
        )

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'djangocms_gallery/{}/item.html'.format(instance.template)
        return template
