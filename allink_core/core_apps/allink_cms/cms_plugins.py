# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _, get_language
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from allink_core.core_apps.allink_cms.models import AllinkPageChooserPlugin, AllinkPage, AllinkLanguageChooserPlugin


class AllinkPageChooserPluginForm(forms.ModelForm):

    class Meta:
        model = AllinkPageChooserPlugin
        exclude = ()


class AllinkPageInline(admin.StackedInline):
    model = AllinkPage
    extra = 0
    verbose_name = 'Page'
    verbose_name_plural = 'Pages'


@plugin_pool.register_plugin
class CMSAllinkPageChooserPlugin(CMSPluginBase):
    model = AllinkPageChooserPlugin

    name = _('Page Chooser')
    module = _('Generic')
    cache = False
    form = AllinkPageChooserPluginForm
    inlines = [AllinkPageInline, ]

    def get_render_template(self, context, instance, placeholder):
        return 'allink_cms/plugins/pagechooser/content.html'

    def render(self, context, instance, placeholder):
        object_list = []
        for page in instance.allinkpage_set.all().order_by('id'):
            if page.page.is_published(get_language()):
                if page.just_descendants:
                    [object_list.append(p) for p in page.page.get_descendants()]
                else:
                    object_list.append(page.page)

        context['object_list'] = object_list
        context['instance'] = instance
        return context


@plugin_pool.register_plugin
class CMSAllinkLanguageChooserPlugin(CMSPluginBase):
    model = AllinkLanguageChooserPlugin

    name = _('Language Chooser')
    module = _('Generic')

    def get_render_template(self, context, instance, placeholder):
        if context['request'].is_ajax() or context['request'].toolbar.edit_mode_active:
            return 'allink_cms/plugins/languagechooser/content.html'
        else:
            return 'allink_cms/plugins/languagechooser/content_skeleton.html'
