# -*- coding: utf-8 -*-
from django.test.testcases import TestCase
from bs4 import BeautifulSoup
from allink_core.core.test import PageApphookMixin, DataModelMixin, DataModelTranslationMixin
from allink_core.apps.news.cms_apps import NewsApphook
from .factories import NewsFactory


class NewsSitemapsTestCase(PageApphookMixin, DataModelMixin, TestCase):
    apphook = 'NewsApphook'
    namespace = 'news'
    page_template = 'default.html'

    apphook_object = NewsApphook
    data_model_factory = NewsFactory

    def test_status_code_200(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)

    def test_all_urls_in_every_language(self):
        response = self.client.get('/sitemap.xml')
        xml = BeautifulSoup(response.content, 'xml').prettify()
        contains = [
            '<xhtml:link href="(.*?){0}(.*?)\/" hreflang="de" rel="alternate"\/>'.format(self.entry_1.slug),
            '<xhtml:link href="(.*?){0}(.*?)\/" hreflang="fr" rel="alternate"\/>'.format(self.entry_1.slug),
        ]
        for text in contains:
            self.assertNotRegex(xml, text)


class NewsSitemapsTranslatedTestCase(PageApphookMixin, DataModelTranslationMixin, TestCase):
    apphook = 'NewsApphook'
    namespace = 'news'
    page_template = 'default.html'

    apphook_object = NewsApphook
    data_model_factory = NewsFactory

    def test_all_urls_with_hreflang_in_every_language(self):
        response = self.client.get('/sitemap.xml')
        xml = BeautifulSoup(response.content, 'xml').prettify()
        contains = [
            '<xhtml:link href="(.*?){0}(.*?)\/" hreflang="en" rel="alternate"\/>'.format(self.entry_1.slug),
            '<xhtml:link href="(.*?){0}(.*?)\/" hreflang="de" rel="alternate"\/>'.format(self.entry_1.slug),
            '<xhtml:link href="(.*?){0}(.*?)\/" hreflang="fr" rel="alternate"\/>'.format(self.entry_1.slug),
        ]
        for text in contains:
            self.assertRegex(xml, text)

    def test_all_urls_with_hreflang_in_every_language_only_for_published_languages(self):
        self.entry_1.delete_translation('de')
        response = self.client.get('/sitemap.xml')
        xml = BeautifulSoup(response.content, 'xml').prettify()
        contains = [
            '<xhtml:link href="(.*?){0}(.*?)\/" hreflang="en" rel="alternate"\/>'.format(self.entry_1.slug),
            '<xhtml:link href="(.*?){0}(.*?)\/" hreflang="fr" rel="alternate"\/>'.format(self.entry_1.slug),
        ]
        for text in contains:
            self.assertRegex(xml, text)
