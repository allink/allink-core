# -*- coding: utf-8 -*-
from allink_core.core.sitemap import HrefLangSitemap
from allink_core.core.loading import get_model

Partner = get_model('partner', 'Partner')


class PartnerSitemap(HrefLangSitemap):
    changefreq = "never"
    priority = 0.5
    i18n = True

    def __init__(self, *args, **kwargs):
        self.namespace = kwargs.pop('namespace', None)
        super(PartnerSitemap, self).__init__(*args, **kwargs)

    def items(self):
        return Partner.objects.translated()

    def lastmod(self, obj):
        return obj.modified
