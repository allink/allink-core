# -*- coding: utf-8 -*-
from allink_core.core.sitemap import HrefLangSitemap
from .models import DummyApp


class DummyAppSitemap(HrefLangSitemap):
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
