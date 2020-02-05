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
            '<xhtml:link href="(.*?)page\/" hreflang="en" rel="alternate"\/>',
            '<xhtml:link href="(.*?)page-de\/" hreflang="de" rel="alternate"\/>',
            '<xhtml:link href="(.*?)page-fr\/" hreflang="fr" rel="alternate"\/>',
        ]
        for text in contains:
            self.assertRegex(xml, text)

    def test_all_urls_with_hreflang_in_every_language_child_page(self):
        response = self.client.get('/sitemap.xml')
        xml = BeautifulSoup(response.content, 'xml').prettify()
        contains = [
            '<xhtml:link href="(.*?)page\/child_page\/" hreflang="en" rel="alternate"\/>',
            '<xhtml:link href="(.*?)page-de\/child_page-de\/" hreflang="de" rel="alternate"\/>',
            '<xhtml:link href="(.*?)page-fr\/child_page-fr\/" hreflang="fr" rel="alternate"\/>',
        ]
        for text in contains:
            self.assertRegex(xml, text)

    def test_all_urls_with_hreflang_in_every_language_only_for_published_languages(self):
        self.child_page.unpublish('de')
        response = self.client.get('/sitemap.xml')
        xml = BeautifulSoup(response.content, 'xml').prettify()
        contains = [
            '<xhtml:link href="(.*?)page\/child_page\/" hreflang="en" rel="alternate"\/>',
            '<xhtml:link href="(.*?)page-fr\/child_page-fr\/" hreflang="fr" rel="alternate"\/>',
        ]
        for text in contains:
            self.assertRegex(xml, text)