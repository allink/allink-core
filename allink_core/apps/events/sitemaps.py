# -*- coding: utf-8 -*-

from allink_core.core.loading import get_model
from allink_core.core.sitemap import HrefLangSitemap


Events = get_model('events', 'Events')


class EventsSitemap(HrefLangSitemap):

    changefreq = "never"
    priority = 0.5
    i18n = True

    def __init__(self, *args, **kwargs):
        self.namespace = kwargs.pop('namespace', None)
        super(EventsSitemap, self).__init__(*args, **kwargs)

    def items(self):
        return Events.objects.translated()

    def lastmod(self, obj):
        return obj.modified
