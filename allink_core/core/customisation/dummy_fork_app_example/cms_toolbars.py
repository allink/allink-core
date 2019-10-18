# -*- coding: utf-8 -*-
"""
use core:
from allink_core.apps.dummy_app.cms_toolbars import *  # noqa
"""
from allink_core.apps.dummy_app.cms_toolbars import *  # noqa

Config = get_model('config', 'Config')

toolbar_pool.unregister(DummyAppToolbar)


class DummyAppToolbar(DummyAppToolbar):
    pass


toolbar_pool.register(DummyAppToolbar)
