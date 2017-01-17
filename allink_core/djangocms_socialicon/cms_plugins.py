# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from allink_core.allink_base.utils import get_additional_templates
from cms.plugin_pool import plugin_pool
from .models import AllinkSocialIconContainerPlugin, AllinkSocialIconPlugin
from .forms import AllinkSocialIconContainerPluginForm, AllinkSocialIconPluginForm

#
@plugin_pool.register_plugin
class CMSAllinkLinkContainerPlugin(CMSPluginBase):
    model = AllinkSocialIconContainerPlugin
    name = _('Social Icon Container')
    module = _("allink")
    cache = False
    allow_children = True
    child_classes = ['CMSAllinkSocialPlugin']
    form = AllinkSocialIconContainerPluginForm

    def get_render_template(self, context, instance, placeholder):
        template = 'djangocms_socialicon/content.html'
        return template

#
@plugin_pool.register_plugin
class CMSAllinkSocialPlugin(CMSPluginBase):
    model = AllinkSocialIconPlugin
    name = _('Social Icon')
    module = _("allink")
    cache = False
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
        template = 'djangocms_socialicon/item.html'
        return template