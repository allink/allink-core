# -*- coding: utf-8 -*-
from cms.plugin_pool import plugin_pool
from allink_core.core.cms_plugins import CMSAllinkBaseAppContentPlugin

from .models import DummyAppAppContentPlugin


@plugin_pool.register_plugin
class CMSDummyAppAppContentPlugin(CMSAllinkBaseAppContentPlugin):
    """
    model:
    - where to store plugin instances

    name:
    - name of the plugin
    """
    model = DummyAppAppContentPlugin
    name = model.data_model._meta.verbose_name_plural
