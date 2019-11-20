# -*- coding: utf-8 -*-
from django.utils.text import slugify
from django.utils.translation import override
from django.test.testcases import TestCase
from django.conf import settings
from django.test.client import RequestFactory
from django.template import Template, RequestContext
from cms import api
from parler.utils.context import switch_language
from allink_core.core.test import PageApphookMixin, CategoriesMixin, DataModelMixin, PluginModelMixin
from allink_core.apps.news.cms_apps import NewsApphook
from allink_core.apps.config.utils import get_fallback
from allink_core.apps.config.tests.factories import ConfigFactory
from ..models import News
from ..cms_plugins import CMSNewsAppContentPlugin
from .factories import NewsFactory, NewsWithMetaFactory


class NewsSitemapsTestCase(PageApphookMixin, DataModelMixin, TestCase):
    apphook = 'NewsApphook'
    namespace = 'news'
    page_template = 'default.html'

    apphook_object = NewsApphook
    data_model_factory = NewsFactory

    def test_status_code_200(self):
        response = self.client.get('sitemap.xml')
        self.assertEqual(response.status_code, 200)

    def test_all_urls_in_every_language(self):
        response = self.client.get('sitemap.xml')
        contains = [
            'rel="alternate" hreflang="en"',
            'rel="alternate" hreflang="de"',
        ]
        for text in contains:
            self.assertContains(response.content, text)

