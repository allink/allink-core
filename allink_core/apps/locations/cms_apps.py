# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class LocationsApphook(CMSApp):
    name = "Locations Apphook"
    app_name = 'locations'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['allink_core.apps.locations.urls']


apphook_pool.register(LocationsApphook)
