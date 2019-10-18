# -*- coding: utf-8 -*-
"""
use core:
from allink_core.apps.dummy_app.cms_menus import *  # noqa
"""
from allink_core.core.loading import unregister_cms_menu
from allink_core.apps.dummy_app.cms_menus import *  # noqa

unregister_cms_menu(DummyAppMenu)


class DummyAppMenu(DummyAppMenu):
    pass


menu_pool.register_menu(get_class('dummy_app.cms_menus', 'DummyAppMenu'))
