# -*- coding: utf-8 -*-

from allink_core.core.loading import get_model
from allink_core.core.sitemap import HrefLangSitemap


News = get_model('news', 'News')


class NewsSitemap(HrefLangSitemap):

    changefreq = "never"
    priority = 0.5
    i18n = True

    def __init__(self, *args, **kwargs):
        self.namespace = kwargs.pop('namespace', None)
        super(NewsSitemap, self).__init__(*args, **kwargs)

    def items(self):
        return News.objects.translated()

    def lastmod(self, obj):
        return obj.modified
