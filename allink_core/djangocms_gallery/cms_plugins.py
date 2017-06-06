# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from webpack_loader.utils import get_files
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

    class Media:
        js = (get_files('djangocms_custom_admin')[0]['publicPath'], )
        css = {
            'all': (get_files('djangocms_custom_admin')[1]['publicPath'], )
        }

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'template',
                ),
            }),
            (_('Slider Options'), {
                'fields': [
                    'ratio',
                    'fullscreen_enabled',
                    'counter_enabled',
                    'auto_start_enabled',
                ]
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
