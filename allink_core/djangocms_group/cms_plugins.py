# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from allink_core.djangocms_group.models import AllinkGroupContainerPlugin, AllinkGroupPlugin
from allink_core.djangocms_group.forms import AllinkGroupContainerPluginForm, AllinkGroupPluginForm


@plugin_pool.register_plugin
class CMSAllinkGroupContainerPlugin(CMSPluginBase):
    model = AllinkGroupContainerPlugin
    name = _('Group Container')
    module = _("allink")
    allow_children = True
    child_classes = ['CMSAllinkGroupPlugin', 'CMSAllinkButtonLinkContainerPlugin']
    form = AllinkGroupContainerPluginForm
    filter_vertical = ('groups', )

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'title',
                    'groups',
                ),
            }),
        )

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'djangocms_group/content.html'
        return template


@plugin_pool.register_plugin
class CMSAllinkGroupPlugin(CMSPluginBase):
    model = AllinkGroupPlugin
    name = _('Group')
    module = _("allink")
    allow_children = True
    child_classes = settings.CMS_ALLINK_GROUP_PLUGIN_CHILD_CLASSES
    form = AllinkGroupPluginForm

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {
                'fields': (
                    'title',
                ),
            }),
        )

        return fieldsets

    def get_render_template(self, context, instance, placeholder):
        template = 'djangocms_group/item.html'
        return template
