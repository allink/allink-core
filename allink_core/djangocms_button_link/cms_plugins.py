# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.templatetags.static import static
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from allink_core.djangocms_button_link.models import AllinkButtonLinkContainerPlugin, AllinkButtonLinkPlugin
from allink_core.djangocms_button_link.forms import AllinkButtonLinkContainerPluginForm, AllinkButtonLinkPluginForm


@plugin_pool.register_plugin
class CMSAllinkButtonLinkContainerPlugin(CMSPluginBase):
    model = AllinkButtonLinkContainerPlugin
    name = _('Button/ Link Container')
    module = _("allink")
    allow_children = True
    child_classes = ['CMSAllinkButtonLinkPlugin']
    form = AllinkButtonLinkContainerPluginForm

    class Media:
        js = (
            'build/djangocms_custom_admin_scripts.js',
        )
        css = {
            'all': (
                'build/djangocms_custom_admin_style.css',

            )
        }

    def get_render_template(self, context, instance, placeholder):
        template = 'djangocms_button_link/content.html'
        return template


@plugin_pool.register_plugin
class CMSAllinkButtonLinkPlugin(CMSPluginBase):
    model = AllinkButtonLinkPlugin
    name = _('Button/ Link')
    module = _("allink")
    allow_children = False
    form = AllinkButtonLinkPluginForm
    change_form_template = 'admin/djangocms_button_link/change_form.html'
    render_template = 'djangocms_button_link/item.html'
    text_enabled = True

    class Media:
        js = (
            'build/djangocms_custom_admin_scripts.js',
        )
        css = {
            'all': (
                'build/djangocms_custom_admin_style.css',

            )
        }

    fieldsets = (
        (None, {
            'fields': (
                'label',
                'type',
                'btn_context',
                # 'txt_context',
                'btn_size',
                # ('icon_left', 'icon_right', 'btn_block',),
            ),
        }),
        (_('Link settings'), {
            # 'classes': ('collapse',),
            'fields': (
                ('link_url', 'link_internal',),
                ('link_mailto', 'link_phone'),
                ('link_anchor', 'link_special'),
                'link_file',
                'link_target',
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                # 'extra_css_classes',
                'link_attributes',
                'project_css_classes',
            )
        }),
    )

    def icon_src(self, instance):
        return static('aldryn_bootstrap3/img/type/button.png')

    def get_render_template(self, context, instance, placeholder):
        template = 'djangocms_button_link/item.html'
        return template

    def render(self, context, instance, placeholder):
        context = super(CMSAllinkButtonLinkPlugin, self).render(context, instance, placeholder)

        return context
