# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import AllinkContentPlugin, AllinkContentColumnPlugin
from .forms import AllinkContentPluginForm, AllinkContentColumnPluginForm


@plugin_pool.register_plugin
class CMSAllinkContentPlugin(CMSPluginBase):
    model = AllinkContentPlugin
    name = _('Content')
    module = _("allink")
    render_template = "djangocms_content/default/content.html"
    cache = False
    allow_children = True
    child_classes = ['ContentColumnPlugin']
    form = AllinkContentPluginForm

    class Media:
        js = ('build/djangocms_custom_admin_scripts.js', )
        css = {
             'all': ('build/djangocms_custom_admin_style.css', )
        }

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'title_size',
                'template',
            ),
        }),
        (_('Display Options'), {
            'classes': ('collapse',),
            'fields': (
                'container_enabled',
                'full_height_enabled',
                'overlay_styles_enabled',
                'bg_color',
            )
        }),
        (_('Full width background image'), {
            'classes': ('collapse',),
            'fields': (
                'bg_image_outer_container',
                'parallax_enabled',
            )
        }),
        (_('Container background image'), {
            'classes': ('collapse',),
            'fields': (
                'bg_image_inner_container',
            )
        }),
        (_('Video background (only works if all fields are set)'), {
            'classes': ('collapse',),
            'fields': (
                'video_file',
                'video_poster_image',
                'video_mobile_image',
                'video_mobile_image_alignment',
            )
        }),
        (_('Advanced Options'), {
            'classes': ('collapse',),
            'fields': (
                'extra_css_classes',
            )
        })
    )

    def save_model(self, request, obj, form, change):
        response = super(CMSAllinkContentPlugin, self).save_model(
            request, obj, form, change
        )
        if obj.numchild == 0:
            column_amount = AllinkContentPlugin.COLUMN_AMOUNT[form.cleaned_data['template']]

            for x in range(int(column_amount)):
                col = AllinkContentColumnPlugin(
                    parent=obj,
                    placeholder=obj.placeholder,
                    language=obj.language,
                    position=CMSPlugin.objects.filter(parent=obj).count(),
                    plugin_type=CMSAllinkContentColumnPlugin.__name__
                )
                col.save()
        return response


@plugin_pool.register_plugin
class CMSAllinkContentColumnPlugin(CMSPluginBase):
    model = AllinkContentColumnPlugin
    name = _("Column")
    module = _("allink")
    render_template = "djangocms_content/default/column.html"
    parent_classes = ["AllinkContentPlugin"]
    allow_children = True
    child_classes = ['TextPlugin', 'PicturePlugin', 'VideoPlayerPlugin', 'VideoSourcePlugin', 'VideoTrackPlugin',
                     'CMSAllinkGalleryPlugin', 'CMSAllinkLinkContainerPlugin', 'CMSAllinkSignupFormPlugin']
    form = AllinkContentColumnPluginForm
    require_parent = True
