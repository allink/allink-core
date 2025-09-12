# -*- coding: utf-8 -*-

from allink_core.core.loading import get_model
from allink_core.core.sitemap import HrefLangSitemap

People = get_model('people', 'People')


class PeopleSitemap(HrefLangSitemap):
    queryset = People.objects.translated()
    changefreq = "never"
    priority = 0.5
    i18n = True

    def __init__(self, *args, **kwargs):
        self.namespace = kwargs.pop('namespace', None)
        super(PeopleSitemap, self).__init__(*args, **kwargs)

    def lastmod(self, obj):
        return obj.modified
