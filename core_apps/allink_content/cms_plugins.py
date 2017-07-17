# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from webpack_loader.utils import get_files

from allink_core.core_apps.allink_content.models import AllinkContentPlugin, AllinkContentColumnPlugin
from allink_core.core_apps.allink_content.forms import AllinkContentPluginForm, AllinkContentColumnPluginForm


@plugin_pool.register_plugin
class CMSAllinkContentPlugin(CMSPluginBase):
    model = AllinkContentPlugin
    name = _('Content')
    module = _('Generic')
    render_template = "allink_content/default/content.html"
    allow_children = True
    child_classes = ['ContentColumnPlugin']
    form = AllinkContentPluginForm

    class Media:
        js = (get_files('djangocms_custom_admin')[0]['publicPath'], )
        css = {
            'all': (get_files('djangocms_custom_admin')[1]['publicPath'], )
        }

    fieldsets = (
        (None, {
            'fields': (
                'title',
                'title_size',
                'template',
            ),
        }),
        (_('Section Options'), {
            'classes': ('collapse',),
            'fields': [
                'container_enabled',
                'full_height_enabled',
                'inverted_colors_enabled',
                'overlay_enabled',
                'bg_color',
            ]
        }),
        (_('Background Image (full width)'), {
            'classes': ('collapse',),
            'fields': (
                'bg_image_outer_container',
                'parallax_enabled',
                'dynamic_height_enabled',
            )
        }),
        (_('Background Image (container)'), {
            'classes': ('collapse',),
            'fields': (
                'bg_image_inner_container',
            )
        }),
        (_('Background Video (Important: Only works if all fields are set)'), {
            'classes': ('collapse',),
            'fields': (
                'video_file',
                'video_poster_image',
                'video_mobile_image',
            )
        }),
        (_('Advanced Options'), {
            'classes': ('collapse',),
            'fields': (
                'project_css_classes',
                'project_on_screen_effect',
                'anchor',
                'ignore_in_pdf',
            )
        })
    )

    def save_model(self, request, obj, form, change):
        response = super(CMSAllinkContentPlugin, self).save_model(request, obj, form, change)
        if obj.numchild == 0:
            column_amount = AllinkContentPlugin.get_template_column_count(form.cleaned_data['template'])

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
    module = _('Generic')
    render_template = "allink_content/default/column.html"
    parent_classes = ["AllinkContentPlugin"]
    allow_children = True
    child_classes = settings.CMS_ALLINK_CONTENT_PLUGIN_CHILD_CLASSES
    form = AllinkContentColumnPluginForm
    require_parent = True

    disable_copyable_menu = True
    disable_cutable_menu = True
    disable_deletable_menu = True

    class Media:
        js = (get_files('djangocms_custom_admin')[0]['publicPath'], )
        css = {
            'all': (get_files('djangocms_custom_admin')[1]['publicPath'], )
        }

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):

        if 'order_mobile' in form.changed_data:
            parent = obj.parent.get_plugin_instance()[0]
            for column in parent.get_children():
                if column.plugin_type == 'CMSAllinkContentColumnPlugin':
                    #  change the column which had the same ordering before
                    #  to the value which our changed column had before
                    child_column = column.get_plugin_instance()[0]
                    if child_column.order_mobile == form.cleaned_data.get('order_mobile'):
                        child_column.order_mobile = form.initial.get('order_mobile')
                        child_column.save()
        return super(CMSAllinkContentColumnPlugin, self).save_model(request, obj, form, change)
