# -*- coding: utf-8 -*-
from cms.plugin_pool import plugin_pool
from allink_core.core.cms_plugins import CMSAllinkBaseAppContentPlugin

from allink_core.core.loading import get_model

NewsAppContentPlugin = get_model('news', 'NewsAppContentPlugin')
KnowledgeAppContentPlugin = get_model('news', 'KnowledgeAppContentPlugin')

@plugin_pool.register_plugin
class CMSNewsAppContentPlugin(CMSAllinkBaseAppContentPlugin):
    """
    model:
    - where to store plugin instances

    name:
    - name of the plugin
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    model = NewsAppContentPlugin
    name = model.data_model._meta.verbose_name_plural


@plugin_pool.register_plugin
class CMSKnowledgeAppContentPlugin(CMSAllinkBaseAppContentPlugin):
    """
    model:
    - where to store plugin instances

    name:
    - name of the plugin
    """
    model = KnowledgeAppContentPlugin
    name = model.data_model._meta.verbose_name_plural
