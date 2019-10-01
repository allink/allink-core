# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class NewsletterApphook(CMSApp):
    name = "Newsletter Apphook"
    app_name = 'newsletter'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['allink_core.apps.newsletter.urls']


apphook_pool.register(NewsletterApphook)
