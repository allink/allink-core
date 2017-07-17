# -*- coding: utf-8 -*-
from cms.plugin_pool import plugin_pool
from allink_core.core.cms_plugins import CMSAllinkBaseAppContentPlugin

from allink_core.core.loading import get_model


TestimonialsAppContentPlugin = get_model('testimonials', 'TestimonialsAppContentPlugin')


@plugin_pool.register_plugin
class CMSTestimonialsAppContentPlugin(CMSAllinkBaseAppContentPlugin):
    """
    model:
    - where to store plugin instances

    name:
    - name of the plugin
    """
    model = TestimonialsAppContentPlugin
    name = model.data_model.get_verbose_name_plural()
