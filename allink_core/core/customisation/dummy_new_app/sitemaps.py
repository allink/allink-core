# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from .models import DummyApp


class DummyAppSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5
    i18n = True

    def __init__(self, *args, **kwargs):
        self.namespace = kwargs.pop('namespace', None)
        super(DummyAppSitemap, self).__init__(*args, **kwargs)

    def items(self):
        return DummyApp.objects.translated()

    def lastmod(self, obj):
        return obj.modified
