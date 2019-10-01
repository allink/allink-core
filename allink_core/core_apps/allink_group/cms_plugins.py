# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from allink_core.core_apps.allink_group.models import AllinkGroupContainerPlugin, AllinkGroupPlugin


class AllinkGroupContainerPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkGroupContainerPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')


class AllinkGroupPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkGroupPlugin
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')


@plugin_pool.register_plugin
class CMSAllinkGroupContainerPlugin(CMSPluginBase):
    model = AllinkGroupContainerPlugin
    name = 'Group Container'
    module = 'Generic'
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
        template = 'allink_group/content.html'
        return template


@plugin_pool.register_plugin
class CMSAllinkGroupPlugin(CMSPluginBase):
    model = AllinkGroupPlugin
    name = 'Group'
    module = 'Generic'
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
        template = 'allink_group/item.html'
        return template
