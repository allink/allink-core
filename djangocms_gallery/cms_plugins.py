# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from allink_core.allink_base.utils import get_additional_templates
from cms.plugin_pool import plugin_pool
from .models import AllinkGalleryPlugin, AllinkGalleryImagePlugin
from .forms import AllinkGalleryPluginForm, AllinkGalleryImagePluginForm


@plugin_pool.register_plugin
class CMSAllinkGalleryPlugin(CMSPluginBase):
    model = AllinkGalleryPlugin
    name = _('Gallery')
    module = _("allink")
    cache = False
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
    cache = False
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
