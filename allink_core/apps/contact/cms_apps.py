# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class ContactApphook(CMSApp):
    name = "Contact Apphook"
    app_name = 'contact'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['allink_core.apps.contact.urls']


apphook_pool.register(ContactApphook)
