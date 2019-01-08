# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.templatetags.static import static
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from webpack_loader.utils import get_files
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
            get_files('djangocms_custom_admin')[0]['publicPath'],
        )
        css = {
            'all': (
                get_files('djangocms_custom_admin')[1]['publicPath'],

            )
        }

    fieldsets = (
        (None, {
            'fields': (
                'alignment_horizontal_desktop',
                'alignment_horizontal_mobile',
            ),
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'project_css_classes',
            )
        }),
    )

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
        js = (get_files('djangocms_custom_admin')[0]['publicPath'], )
        css = {
            'all': (get_files('djangocms_custom_admin')[1]['publicPath'], )
        }

    fieldsets = (
        (None, {
            'fields': (
                'template',
                'label',
                'type',
                'btn_context',
                # 'txt_context',
                'btn_size',
                # ('icon_left', 'icon_right', 'btn_block',),
            ),
        }),
        (_('Internal/External link settings'), {
            'classes': (
                'only_when_default_link',
            ),
            'fields': (
                'internal_link',
                'link_url',
                'link_anchor',
                'link_target_reduced',
            )
        }),
        (_('File link settings'), {
            'classes': (
                'only_when_file_link',
                'only_when_image_link',
            ),
            'fields': (
                'link_file',
            )
        }),
        (_('Phone link settings'), {
            'classes': (
                'only_when_phone_link',
            ),
            'fields': (
                'link_phone',
            )
        }),
        (_('Email link settings'), {
            'classes': (
                'only_when_email_link',
            ),
            'fields': (
                'link_mailto',
                'email_subject',
                'email_body_text',
            )
        }),
        (_('Form link settings'), {
            'classes': (
                'only_when_form_link',
            ),
            'fields': (
                'link_special',
            )
        }),
        (_('Video (Embedded) link settings'), {
            'classes': (
                'only_when_video_embedded_link',
            ),
            'fields': (
                'video_id',
                'video_service',
                'ratio',
                'auto_start_enabled',
                'allow_fullscreen_enabled',
            )
        }),
        # (_('Video (File) link settings'), {
        #     'classes': (
        #         'only_when_video_file_link',
        #     ),
        #     'fields': (
        #
        #     )
        # }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                # 'extra_css_classes',
                'link_attributes',
            )
        }),
        (_('Hidden settings'), {
            'classes': ('hidden',),
            'fields': (
                # 'extra_css_classes',
                'link_target',
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
