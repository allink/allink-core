# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap

from allink_core.core.loading import get_model

People = get_model('people', 'People')


class PeopleSitemap(Sitemap):

    changefreq = "never"
    priority = 0.5
    i18n = True

    def __init__(self, *args, **kwargs):
        self.namespace = kwargs.pop('namespace', None)
        super(PeopleSitemap, self).__init__(*args, **kwargs)

    def items(self):
        return People.objects.active()

    def lastmod(self, obj):
        return obj.modified
