# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.templatetags.static import static
from cms.plugin_base import CMSPluginBase
from allink_core.allink_base.utils import get_additional_templates
from cms.plugin_pool import plugin_pool
from .models import AllinkButtonLinkContainerPlugin, AllinkButtonLinkPlugin
from .forms import AllinkButtonLinkContainerPluginForm, AllinkButtonLinkPluginForm

#
@plugin_pool.register_plugin
class CMSAllinkButtonLinkContainerPlugin(CMSPluginBase):
    model = AllinkButtonLinkContainerPlugin
    name = _('Button/ Link Container')
    module = _("allink")
    cache = False
    allow_children = True
    child_classes = ['CMSAllinkButtonLinkPlugin']
    form = AllinkButtonLinkContainerPluginForm

    def get_render_template(self, context, instance, placeholder):
        template = 'djangocms_button_link/content.html'
        return template

#
@plugin_pool.register_plugin
class CMSAllinkButtonLinkPlugin(CMSPluginBase):
    model = AllinkButtonLinkPlugin
    name = _('Button/ Link')
    module = _("allink")
    cache = False
    allow_children = False
    form = AllinkButtonLinkPluginForm
    text_enabled = False
    change_form_template = 'admin/djangocms_button_link/change_form.html'
    render_template = 'djangocms_button_link/button.html'
    text_enabled = True
    allow_children = True

    class Media:
        js = (
            'build/djangocms_custom_admin_scripts.js',
            'aldryn_bootstrap3/js/jquery.min.js',
            'aldryn_bootstrap3/js/bootstrap.min.js',
            'aldryn_bootstrap3/js/iconset/iconset-glyphicon.min.js',
            'aldryn_bootstrap3/js/iconset/iconset-fontawesome-4.2.0.min.js',
            'aldryn_bootstrap3/js/bootstrap-iconpicker.min.js',
            'aldryn_bootstrap3/js/base.js',
        )
        css = {
             'all': (
                 'build/djangocms_custom_admin_style.css',
                 'aldryn_bootstrap3/css/bootstrap.min.css',
                 'aldryn_bootstrap3/css/bootstrap-iconpicker.min.css',
                 'aldryn_bootstrap3/css/font-awesome.min.css',
                 'aldryn_bootstrap3/css/base.css',

             )
        }

    fieldsets = (
        (None, {
            'fields': (
                'type',
                'label',
                'btn_context',
                'txt_context',
                'btn_size',
                ('icon_left', 'icon_right', 'btn_block',),
            ),
        }),
        (_('Link settings'), {
            'classes': ('collapse',),
            'fields': (
                ('link_url', 'link_page',),
                ('link_mailto', 'link_phone'),
                ('link_anchor', 'link_target'),
                'link_file',
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'extra_css_classes',
                'link_attributes',
            )
        }),
    )

    def icon_src(self, instance):
        return static('aldryn_bootstrap3/img/type/button.png')

    def get_render_template(self, context, instance, placeholder):
        template = 'djangocms_button_link/button.html'
        return template
