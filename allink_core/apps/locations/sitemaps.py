# -*- coding: utf-8 -*-

from allink_core.core.loading import get_model
from allink_core.core.sitemap import HrefLangSitemap


Locations = get_model('locations', 'Locations')


class LocationsSitemap(HrefLangSitemap):

    changefreq = "never"
    priority = 0.5
    i18n = True

    def __init__(self, *args, **kwargs):
        self.namespace = kwargs.pop('namespace', None)
        super(LocationsSitemap, self).__init__(*args, **kwargs)

    def items(self):
        return Locations.objects.translated()

    def lastmod(self, obj):
        return obj.modified
