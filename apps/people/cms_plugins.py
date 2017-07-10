# -*- coding: utf-8 -*-
from cms.plugin_pool import plugin_pool
from allink_core.core.cms_plugins import CMSAllinkBaseAppContentPlugin

from allink_core.core.loading import get_model


PeopleAppContentPlugin = get_model('people', 'PeopleAppContentPlugin')


@plugin_pool.register_plugin
class CMSPeoplePlugin(CMSAllinkBaseAppContentPlugin):
    """
    model:
    - where to store plugin instances

    name:
    - name of the plugin
    """
    model = PeopleAppContentPlugin
    name = model.data_model.get_verbose_name_plural()
