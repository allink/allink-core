# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from allink_core.core.cms_plugins import CMSAllinkBaseAppContentPlugin

from allink_core.core.loading import get_model, get_class


WorkAppContentPlugin = get_model('work', 'WorkAppContentPlugin')
Work = get_model('work', 'Work')
WorkSearchPlugin = get_model('work', 'WorkSearchPlugin')
WorkSearchForm = get_class('work.forms', 'WorkSearchForm')


@plugin_pool.register_plugin
class CMSWorkPlugin(CMSAllinkBaseAppContentPlugin):
    """
    model:
    - where to store plugin instances

    name:
    - name of the plugin
    """
    model = WorkAppContentPlugin
    name = model.data_model.get_verbose_name_plural()


@plugin_pool.register_plugin
class CMSWorkSearchPlugin(CMSPluginBase):
    model = WorkSearchPlugin
    render_template = 'work/plugins/search/content.html'
    name = _(u'{} Search'.format(model.data_model.get_verbose_name_plural()))
    module = _(u'allink Apps')

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['placeholder'] = placeholder

        form = WorkSearchForm()
        object_list = self.model.data_model.objects.active()

        additional_context = [
            ('form', form),
            ('object_list', object_list),
        ]

        for key, val in additional_context:
            context.update({key: val})

        return context
