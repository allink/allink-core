# -*- coding: utf-8 -*-
"""
use core:
from allink_core.apps.dummy_app.cms_plugins import *  # noqa
"""
from allink_core.apps.dummy_app.cms_plugins import *  # noqa

plugin_pool.unregister_plugin(CMSDummyAppAppContentPlugin)


@plugin_pool.register_plugin
class CMSDummyAppAppContentPlugin(CMSDummyAppAppContentPlugin):

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        context.update({
            'some': 'stuff',
        })

        return context
