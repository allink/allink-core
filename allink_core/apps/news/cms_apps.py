# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class NewsApphook(CMSApp):
    name = "News Apphook"
    app_name = 'news'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['allink_core.apps.news.urls']


apphook_pool.register(NewsApphook)
