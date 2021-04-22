# -*- coding: utf-8 -*-
from django.utils.text import slugify
from django.utils.translation import override
from django.test.testcases import TestCase
from django.conf import settings
from django.test.client import RequestFactory
from django.template import Template, RequestContext
from cms import api
from parler.utils.context import switch_language
from allink_core.core.test import PageApphookMixin, CategoriesMixin, DataModelMixin, AllinkAppContenPluginMixin
from allink_core.apps.news.cms_apps import NewsApphook
from allink_core.apps.config.utils import get_fallback
from allink_core.apps.config.tests.factories import ConfigFactory
from ..models import News
from ..cms_plugins import CMSNewsAppContentPlugin
from .factories import NewsFactory, NewsWithMetaFactory


class NewsTestCase(PageApphookMixin, DataModelMixin, TestCase):

    apphook = 'NewsApphook'
    namespace = 'news'
    page_template = 'default.html'

    apphook_object = NewsApphook
    data_model_factory = NewsFactory

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
            'page', self.page_template,
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
        with override('de'):
            self.assertEqual(
                self.entry_1.get_absolute_url(),
                '{}{}/'.format(self.page.get_absolute_url(), self.entry_1.safe_translation_getter('slug', language_code='de'))
            )
            self.assertIn('/de/', self.entry_1.get_absolute_url())


class NewsMetaTestCase(TestCase):

    def setUp(self):
        self.entry_1 = NewsWithMetaFactory()
        self.allink_config = ConfigFactory()

    def render_template(self, string, request, context=None):
        context = context or {}
        context = RequestContext(request, context)
        context.request = request
        return Template(string).render(context)

    def test_get_page_title_with_appropriate_fallbacks(self):
        self.assertEqual(self.entry_1.meta_page_title, 'og title | default_base_title_en')

        self.entry_1.og_title = ''
        self.assertEqual(self.entry_1.meta_page_title, 'teaser title | default_base_title_en')

        self.entry_1.teaser_title = ''
        self.assertEqual(self.entry_1.meta_page_title, '{} | default_base_title_en'.format(self.entry_1.title))

        # remove default_base_title_en from allink_config
        self.allink_config.default_base_title = ''
        # also remove default translation 'en'
        with switch_language(self.allink_config, 'en'):
            self.allink_config.default_base_title = ''
            self.allink_config.save()
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
            'meta_image_url': getattr(self.entry_1.meta_image_thumb, 'url', ''),
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
        self.assertIn('1200x630', rendered_template)
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


class NewsTeaserTestCase(TestCase):

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
            'teaser_link': '/no_apphook_configured',
            'teaser_link_url': None,
            'teaser_link_url': None,
        }
        self.assertDictEqual(expected_meta_context, self.entry_1.teaser_dict)


class NewsPluginTestCaseApp(CategoriesMixin, DataModelMixin, AllinkAppContenPluginMixin, TestCase):
    apphook = 'NewsApphook'
    namespace = 'news'
    page_template = 'default.html'
    apphook_object = NewsApphook
    data_model_factory = NewsFactory
    plugin_class = CMSNewsAppContentPlugin

    def test_no_filter_no_manual_select(self):
        self.assertEqual(self.plugin_model_instance.get_render_queryset_for_display().count(), 5)

    def test_no_filter_manual_select(self):
        self.plugin_model_instance.manual_entries.set([self.entry_1, self.entry_2])
        self.assertEqual(self.plugin_model_instance.get_render_queryset_for_display().count(), 2)

    def test_no_filter_manual_select_filter_category(self):
        self.plugin_model_instance.manual_entries.set([self.entry_1, self.entry_2, self.entry_3])

        self.entry_1.categories.set([self.category_1, self.category_2])
        self.entry_2.categories.set([self.category_1, self.category_2])

        self.assertEqual(self.plugin_model_instance.get_render_queryset_for_display().count(), 3)
        self.assertEqual(self.plugin_model_instance.get_render_queryset_for_display(category=self.category_1).count(), 2)

    def test_filter_category(self):
        self.plugin_model_instance.categories.set([self.category_1])

        self.entry_1.categories.set([self.category_1, self.category_2])
        self.entry_2.categories.set([self.category_1, self.category_2])

        self.assertEqual(self.plugin_model_instance.get_render_queryset_for_display().count(), 2)
        self.assertEqual(self.plugin_model_instance.get_render_queryset_for_display(category=self.category_1).count(), 2)

    def test_filter_category_multiple_categories_set(self):
        self.plugin_model_instance.categories.set([self.category_1, self.category_2])

        self.entry_1.categories.set([self.category_1, self.category_2])
        self.entry_2.categories.set([self.category_1, self.category_2])
        self.entry_3.categories.set([self.category_2])

        self.assertEqual(self.plugin_model_instance.get_render_queryset_for_display().count(), 3)
        self.assertEqual(self.plugin_model_instance.get_render_queryset_for_display(category=self.category_1).count(), 2)
        self.assertEqual(self.plugin_model_instance.get_render_queryset_for_display(category=self.category_2).count(), 3)

    def test_filter_filters_categories_and__in_no_result(self):
        self.plugin_model_instance.categories.set([self.category_1])
        self.plugin_model_instance.categories_and.set([self.category_2])

        self.entry_1.categories.set([self.category_1])
        self.entry_2.categories.set([self.category_2])
        self.assertEqual(self.plugin_model_instance.get_render_queryset_for_display().count(), 0)

    def test_filter_filters_categories_and__in_result(self):
        self.plugin_model_instance.categories.set([self.category_1])
        self.plugin_model_instance.categories_and.set([self.category_2])

        self.entry_1.categories.set([self.category_1])
        self.entry_2.categories.set([self.category_2])
        self.entry_3.categories.set([self.category_1, self.category_2])
        self.assertEqual(self.plugin_model_instance.get_render_queryset_for_display().count(), 1)
        self.assertEqual(self.plugin_model_instance.get_render_queryset_for_display().first().id, self.entry_3.id)


