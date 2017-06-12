# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from webpack_loader.utils import get_files
from allink_core.djangocms_gallery.models import AllinkGalleryPlugin, AllinkGalleryImagePlugin
from allink_core.djangocms_gallery.forms import AllinkGalleryPluginForm, AllinkGalleryImagePluginForm
from allink_core.allink_config.models import AllinkConfig


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
            (_('Advanced Options'), {
                'classes': ('collapse',),
                'fields': (
                    'project_css_classes',
                )
            })
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

    class Media:
        js = (get_files('djangocms_custom_admin')[0]['publicPath'], )
        css = {
            'all': (get_files('djangocms_custom_admin')[1]['publicPath'], )
        }

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'image',
                    'title',
                    'text',
                ),
            }),
        )

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        context = super(CMSAllinkGalleryImagePlugin, self).render(context, instance, placeholder)
        context['caption_text_styling_disabled'] = AllinkConfig.get_solo().gallery_plugin_caption_text_styling_disabled
        template = 'djangocms_gallery/{}/item.html'.format(instance.template)
        return template
