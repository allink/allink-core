# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from bs4 import BeautifulSoup
from allink_core.core.test import PageApphookMixin
from allink_core.apps.news.cms_apps import NewsApphook


class CMSHrefLangSitemapTestCase(PageApphookMixin, TestCase):
    apphook = 'NewsApphook'
    namespace = 'news'
    page_template = 'default.html'

    apphook_object = NewsApphook

    def test_status_code_200(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)

    def test_all_urls_with_hreflang_in_every_language(self):
        response = self.client.get('/sitemap.xml')
        xml = BeautifulSoup(response.content, 'xml').prettify()
        contains = [
            '<link href="(.*?)page\/" hreflang="en" rel="alternate"\/>',
            '<link href="(.*?)page-de\/" hreflang="de" rel="alternate"\/>',
            '<link href="(.*?)page-fr\/" hreflang="fr" rel="alternate"\/>',
        ]
        for text in contains:
            self.assertRegex(xml, text)