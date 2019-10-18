# -*- coding: utf-8 -*-
"""
use core:
from allink_core.apps.dummy_app.cms_apps import *  # noqa
"""
from allink_core.core.loading import unregister_cms_apps
from allink_core.apps.dummy_app.cms_apps import *  # noqa

unregister_cms_apps(DummyAppApphook)


class DummyAppApphook(DummyAppApphook):
    def get_urls(self, page=None, language=None, **kwargs):
        urls = super().get_urls(**kwargs)
        return urls + ['apps.dummy_app.urls']


apphook_pool.register(DummyAppApphook)
