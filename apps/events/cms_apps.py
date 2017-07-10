# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class EventsApphook(CMSApp):
    name = _("Events Apphook")
    app_name = 'events'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['allink_core.apps.events.urls']


apphook_pool.register(EventsApphook)
