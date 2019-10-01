# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class EventsApphook(CMSApp):
    name = "Events Apphook"
    app_name = 'events'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['allink_core.apps.events.urls']


apphook_pool.register(EventsApphook)
