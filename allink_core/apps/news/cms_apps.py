# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class NewsApphook(CMSApp):
    name = _("News Apphook")
    app_name = 'news'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['allink_core.apps.news.urls']


apphook_pool.register(NewsApphook)