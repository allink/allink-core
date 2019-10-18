# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class DummyAppApphook(CMSApp):
    name = _("DummyApp Apphook")
    app_name = 'dummy_app'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['apps.dummy_app.urls']


apphook_pool.register(DummyAppApphook)
