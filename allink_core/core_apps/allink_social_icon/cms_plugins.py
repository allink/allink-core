# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from allink_core.core.utils import get_additional_choices
from allink_core.core_apps.allink_social_icon.models import AllinkSocialIconContainerPlugin, AllinkSocialIconPlugin
from allink_core.core_apps.allink_social_icon.forms import AllinkSocialIconContainerPluginForm, AllinkSocialIconPluginForm


@plugin_pool.register_plugin
class CMSAllinkSocialIconContainerPlugin(CMSPluginBase):
    model = AllinkSocialIconContainerPlugin
    name = _('Social Icon Container')
    module = _('Generic')
    allow_children = True
    child_classes = ['CMSAllinkSocialIconPlugin']
    form = AllinkSocialIconContainerPluginForm
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = ()
        if get_additional_choices('SOCIAL_ICON_CSS_CLASSES'):
            fieldsets = (
                (None, {
                    'fields': (
                        'project_css_classes',
                    ),
                }),
            )

        return fieldsets


    def get_render_template(self, context, instance, placeholder):
        template = 'allink_social_icon/content.html'
        return template


@plugin_pool.register_plugin
class CMSAllinkSocialIconPlugin(CMSPluginBase):
    model = AllinkSocialIconPlugin
    name = _('Social Icon')
    module = _('Generic')
    allow_children = False
    form = AllinkSocialIconPluginForm
    text_enabled = False

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'title',
                    'icon',
                    'link',
                ),
            }),
        )

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'allink_social_icon/item.html'
        return template
