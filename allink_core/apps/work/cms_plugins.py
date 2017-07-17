# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from allink_core.core.cms_plugins import CMSAllinkBaseAppContentPlugin, CMSAllinkBaseSearchPlugin

from allink_core.core.loading import get_model, get_class


WorkAppContentPlugin = get_model('work', 'WorkAppContentPlugin')
Work = get_model('work', 'Work')
WorkSearchPlugin = get_model('work', 'WorkSearchPlugin')
WorkSearchForm = get_class('work.forms', 'WorkSearchForm')


@plugin_pool.register_plugin
class CMSWorkAppContentPlugin(CMSAllinkBaseAppContentPlugin):
    """
    model:
    - where to store plugin instances

    name:
    - name of the plugin
    """
    model = WorkAppContentPlugin
    name = model.data_model.get_verbose_name_plural()


@plugin_pool.register_plugin
class CMSWorkSearchPlugin(CMSAllinkBaseSearchPlugin):
    """
    model:
    - where to store plugin instances

    search_form
    - the form the user supplies the search query

    name:
    - name of the plugin
    """
    model = WorkSearchPlugin
    search_form = WorkSearchForm
    name = _(u'{} Search'.format(model.data_model.get_verbose_name_plural()))
