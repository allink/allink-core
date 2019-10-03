from django.test.testcases import TestCase
from django.test.client import RequestFactory
from django.template import Template, RequestContext
from cms import api
from allink_core.apps.news.tests.factories import NewsFactory
from .factories import ConfigFactory
from ..utils import get_meta_page_title, get_fallback


class AllinkSEOMetaTestCase(TestCase):

    def setUp(self):
        self.page_de = api.create_page(
            title='page title',
            template='default.html',
            language='de',
            published=True,
        )
        self.allink_config = ConfigFactory()
        self.entry_1 = NewsFactory()

    def render_template(self, string, request, context=None):
        context = context or {}
        context = RequestContext(request, context)
        context.request = request
        return Template(string).render(context)

    def test_rendered_template_with_page_contains_correct_values(self):
        request = RequestFactory().get(self.page_de.get_absolute_url())
        request.current_page = self.page_de

        rendered_template = self.render_template(
            string='{% load allink_meta_tags %} {% render_meta_og %}',
            request=request,
        )
        self.assertIn(get_meta_page_title(self.page_de), rendered_template)
        self.assertIn(get_fallback(self.page_de, 'meta_title'), rendered_template)
        self.assertIn(get_fallback(self.page_de, 'meta_description') or '', rendered_template)
        self.assertIn(getattr(get_fallback(self.page_de, 'meta_image'), 'url'), rendered_template)
        self.assertIn(self.allink_config.google_site_verification, rendered_template)

    def test_rendered_template_with_page_contains_correct_overwitten_values(self):
        request = RequestFactory().get(self.page_de.get_absolute_url())
        request.current_page = self.page_de

        rendered_template = self.render_template(
            string='''
            {% load allink_meta_tags %} 
            {% render_meta_og overwrite_dict="{'meta_title': 'Hello', 'meta_description': 'Some Text', 'meta_image_url':'www.foo.ch/image.jpg'}" %}''',
            request=request,
        )
        self.assertIn('Hello', rendered_template)
        self.assertIn(get_fallback(self.page_de, 'meta_title'), rendered_template)
        self.assertIn('Some Text', rendered_template)
        self.assertIn('www.foo.ch/image.jpg', rendered_template)
        self.assertIn(self.allink_config.google_site_verification, rendered_template)
