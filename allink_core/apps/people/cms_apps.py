# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class PeopleApphook(CMSApp):
    name = "People Apphook"
    app_name = 'people'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['allink_core.apps.people.urls']


apphook_pool.register(PeopleApphook)
