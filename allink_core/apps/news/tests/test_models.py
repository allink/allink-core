# -*- coding: utf-8 -*-
from django.utils.text import slugify
from django.utils.translation import override
from django.test.testcases import TransactionTestCase
from django.conf import settings
from django.test.client import RequestFactory
from django.template import Template, RequestContext
from cms import api
from parler.utils.context import switch_language
from allink_core.core.test import DefaultApphookTestCase
from allink_core.apps.news.cms_apps import NewsApphook
from allink_core.apps.config.utils import get_fallback
from allink_core.apps.config.tests.factories import ConfigFactory
from ..models import News
from .factories import NewsFactory, NewsWithMetaFactory


class NewsTestCase(DefaultApphookTestCase):

    apphook = 'NewsApphook'
    namespace = 'news'
    template = 'default.html'

    apphook_object = NewsApphook

    def setUp(self):
        super().setUp()
        self.entry_1 = NewsFactory()

    def test_create_instance(self):
        self.assertEqual(self.entry_1.status, News.ACTIVE)

    def test_delete_instance(self):
        News.objects.get(id=self.entry_1.id).delete()
        with self.assertRaises(News.DoesNotExist):
            News.objects.get(id=self.entry_1.id)

    def test___str__(self):
        self.assertEqual(self.entry_1.__str__(), '{} - {}'.format(
            self.entry_1.title,
            self.entry_1.entry_date.strftime('%d.%m.%Y %H:%M:%S')
        ))

    def test_slug(self):
        self.assertEqual(self.entry_1.slug, slugify(self.entry_1.title))

    def test_get_detail_view(self):
        self.assertEqual(self.entry_1.get_detail_view(), '{}:detail'.format(self.entry_1._meta.model_name))
        self.assertEqual(self.entry_1.get_detail_view('apphook_page'), 'apphook_page:detail')

    def test_get_absolute_url(self):
        self.assertEqual(self.entry_1.get_absolute_url(), '{}{}/'.format(
            self.page.get_absolute_url(), self.entry_1.slug))

    def test_get_absolute_url_no_apphook_configured(self):
        self.page.unpublish(language=self.language)
        self.assertEqual(self.entry_1.get_absolute_url(), '/no_apphook_configured')

    def test_get_absolute_url_specifc_application_namespace(self):
        other_page = api.create_page(
            'page', self.template,
            self.language,
            published=True,
            parent=self.root_page,
            apphook=self.apphook,
            apphook_namespace='some_application_namespace'
        )
        self.assertEqual(self.entry_1.get_absolute_url(application_namespace=other_page.application_namespace), '{}{}/'.format(
            other_page.get_absolute_url(), self.entry_1.slug))

    def test_get_absolute_url_language_fallback(self):
        # no translations
        # known_translation_getter returns 'en'
        with override('de'):
            self.assertEqual(self.entry_1.get_absolute_url(), '{}{}/'.format(
                self.page.get_absolute_url(language='en'), self.entry_1.safe_translation_getter('slug', language_code='en')))
            self.assertIn('/en/', self.entry_1.get_absolute_url())

    def test_get_absolute_url_language_translated(self):
        # translate entry in all languages
        for language, _ in settings.LANGUAGES[1:]:
            with switch_language(self.entry_1, language):
                self.entry_1.title = '{}: {}'.format(self.entry_1.title, language)
                self.entry_1.save()

        # known_translation_getter returns 'de'
        from django.core.cache import cache
        self.reload_urls()
        cache.clear()
        with override('de'):
            self.assertEqual(
                self.entry_1.get_absolute_url(),
                '{}{}/'.format(self.page.get_absolute_url(language='de'), self.entry_1.safe_translation_getter('slug', language_code='de'))
            )
            self.assertIn('/de/', self.entry_1.get_absolute_url())


class NewsMetaTestCase(TransactionTestCase):

    def setUp(self):
        self.entry_1 = NewsWithMetaFactory()
        self.allink_config = ConfigFactory()

    def render_template(self, string, request, context=None):
        context = context or {}
        context = RequestContext(request, context)
        context.request = request
        return Template(string).render(context)

    def test_get_page_title_with_appropriate_fallbacks(self):
        self.assertEqual(self.entry_1.meta_page_title, 'og title | default base title')

        self.entry_1.og_title = ''
        self.assertEqual(self.entry_1.meta_page_title, 'teaser title | default base title')

        self.entry_1.teaser_title = ''
        self.assertEqual(self.entry_1.meta_page_title, '{} | default base title'.format(self.entry_1.title))

        # remove default base title from allink_config
        self.allink_config.default_base_title = ''
        self.allink_config.save()
        self.assertEqual(self.entry_1.meta_page_title, '{} | '.format(self.entry_1.title))

    def test_get_meta_title_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.entry_1, 'meta_title'), 'og title')
        self.entry_1.og_title = ''
        self.assertEqual(get_fallback(self.entry_1, 'meta_title'), 'teaser title')
        self.entry_1.teaser_title = ''
        self.assertEqual(get_fallback(self.entry_1, 'meta_title'), self.entry_1.title)

    def test_get_meta_description_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.entry_1, 'meta_description'), 'og description')
        self.entry_1.og_description = ''
        self.assertEqual(get_fallback(self.entry_1, 'meta_description'), 'teaser description')
        self.entry_1.teaser_description = ''
        self.assertEqual(get_fallback(self.entry_1, 'meta_description'), self.entry_1.lead)

    def test_get_meta_image_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.entry_1, 'meta_image'), self.entry_1.og_image)
        self.entry_1.og_image = None
        self.assertEqual(get_fallback(self.entry_1, 'meta_image'), self.entry_1.teaser_image)
        self.entry_1.teaser_image = None
        self.assertEqual(get_fallback(self.entry_1, 'meta_image'), self.entry_1.preview_image)

    def test_get_meta_dict(self):
        expected_meta_context = {
            'meta_page_title': self.entry_1.meta_page_title,
            'meta_og_title': get_fallback(self.entry_1, 'meta_title'),
            'meta_description': get_fallback(self.entry_1, 'meta_description'),
            'meta_image_url': getattr(get_fallback(self.entry_1, 'meta_image'), 'url', ''),
            'google_site_verification': self.allink_config.google_site_verification,
        }
        self.assertDictEqual(expected_meta_context, self.entry_1.meta_dict)

    def test_render_meta_og_templatetag_with_object_contains_correct_values(self):
        request = RequestFactory().get(self.entry_1.get_absolute_url())
        rendered_template = self.render_template(
            string='''
            {% load allink_meta_tags %}
            {% render_meta_og obj=obj %}''',
            request=request,
            context={'obj': self.entry_1}
        )
        self.assertIn(self.entry_1.meta_page_title, rendered_template)
        self.assertIn(get_fallback(self.entry_1, 'meta_title'), rendered_template)
        self.assertIn(get_fallback(self.entry_1, 'meta_description'), rendered_template)
        self.assertIn(get_fallback(self.entry_1, 'meta_image').url, rendered_template)
        self.assertIn(self.allink_config.google_site_verification, rendered_template)

    def test_rendered_template_with_object_contains_correct_overwitten_values(self):
        request = RequestFactory().get(self.entry_1.get_absolute_url())
        rendered_template = self.render_template(
            string='''
            {% load allink_meta_tags %}
            {% render_meta_og obj=obj overwrite_dict="{'meta_title': 'Hello', 'meta_description': 'Some Text', 'meta_image_url':'www.foo.ch/image.jpg'}" %}''',
            request=request,
            context={'obj': self.entry_1}
        )
        self.assertIn('Hello', rendered_template)
        self.assertIn(get_fallback(self.entry_1, 'meta_title'), rendered_template)
        self.assertIn('Some Text', rendered_template)
        self.assertIn('www.foo.ch/image.jpg', rendered_template)
        self.assertIn(self.allink_config.google_site_verification, rendered_template)


class NewsTeaserTestCase(TransactionTestCase):

    def setUp(self):
        self.entry_1 = NewsWithMetaFactory()
        self.allink_config = ConfigFactory()

    def test_teaser_title_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.entry_1, 'teaser_title'), 'teaser title')

        self.entry_1.teaser_title = ''
        self.assertEqual(get_fallback(self.entry_1, 'teaser_title'), self.entry_1.title)

    def test_teaser_description_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.entry_1, 'teaser_description'), 'teaser description')

        self.entry_1.teaser_description = ''
        self.assertEqual(get_fallback(self.entry_1, 'teaser_description'), self.entry_1.lead)

    def test_teaser_technical_title_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.entry_1, 'teaser_technical_title'), 'teaser technical title')

        self.entry_1.teaser_technical_title = ''
        self.assertEqual(get_fallback(self.entry_1, 'teaser_technical_title'), self.entry_1.entry_date)

    def test_teaser_link_text_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.entry_1, 'teaser_link_text'), 'teaser link text')

        self.entry_1.teaser_link_text = ''
        self.assertEqual(get_fallback(self.entry_1, 'teaser_link_text'), 'Read more')

    def test_teaser_image_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.entry_1, 'teaser_image'), self.entry_1.teaser_image)

        self.entry_1.teaser_image = None
        self.assertEqual(get_fallback(self.entry_1, 'teaser_image'), self.entry_1.preview_image)

    def test_teaser_dict(self):

        expected_meta_context = {
            'teaser_title': get_fallback(self.entry_1, 'teaser_title'),
            'teaser_technical_title': get_fallback(self.entry_1, 'teaser_technical_title'),
            'teaser_description': get_fallback(self.entry_1, 'teaser_description'),
            'teaser_image': get_fallback(self.entry_1, 'teaser_image'),
            'teaser_link_text': get_fallback(self.entry_1, 'teaser_link_text'),
            'teaser_link': self.entry_1.get_absolute_url(),
        }
        self.assertDictEqual(expected_meta_context, self.entry_1.teaser_dict)
