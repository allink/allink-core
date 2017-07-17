# -*- coding: utf-8 -*-
from cms.plugin_pool import plugin_pool
from allink_core.core.cms_plugins import CMSAllinkBaseAppContentPlugin

from allink_core.core.loading import get_model


NewsAppContentPlugin = get_model('news', 'NewsAppContentPlugin')


@plugin_pool.register_plugin
class CMSNewsAppContentPlugin(CMSAllinkBaseAppContentPlugin):
    """
    model:
    - where to store plugin instances

    name:
    - name of the plugin
    """
    model = NewsAppContentPlugin
    name = model.data_model.get_verbose_name_plural()

    @classmethod
    def get_render_queryset(cls):
        return cls.model._default_manager.all()
