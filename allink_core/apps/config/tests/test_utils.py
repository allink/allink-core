from django.test.testcases import TestCase
from cms import api
from .factories import ConfigFactory, AllinkPageExtensionFactory, AllinkTitleExtensionFactory
from ..utils import get_meta_page_title, get_page_meta_dict, get_page_teaser_dict, get_fallback


class AllinkExtensionMetaTestCase(TestCase):

    def setUp(self):
        self.page_de = api.create_page(
            title='page title',
            template='default.html',
            language='de',
            published=True,
        )
        self.allink_config = ConfigFactory()

    def test_get_page_title_with_appropriate_fallbacks(self):
        self.assertEqual(get_meta_page_title(self.page_de), 'page title | default base title')

        # add page extensions
        AllinkTitleExtensionFactory(extended_object=self.page_de.get_title_obj())

        self.assertEqual(get_meta_page_title(self.page_de), 'og title | default base title')

        self.page_de.get_title_obj().allinktitleextension.og_title = ''
        self.assertEqual(get_meta_page_title(self.page_de), 'teaser title | default base title')

        self.page_de.get_title_obj().allinktitleextension.teaser_title = ''
        self.assertEqual(get_meta_page_title(self.page_de), 'page title | default base title')

        # remove default base title from allink_config
        self.allink_config.default_base_title = ''
        self.allink_config.save()
        self.assertEqual(get_meta_page_title(self.page_de), 'page title | ')

    def test_get_meta_title_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.page_de, 'meta_title'), 'page title')

        # add page extensions
        AllinkTitleExtensionFactory(extended_object=self.page_de.get_title_obj())

        self.assertEqual(get_fallback(self.page_de, 'meta_title'), 'og title')

        self.page_de.get_title_obj().allinktitleextension.og_title = ''
        self.assertEqual(get_fallback(self.page_de, 'meta_title'), 'teaser title')

        self.page_de.get_title_obj().allinktitleextension.teaser_title = ''
        self.assertEqual(get_fallback(self.page_de, 'meta_title'), 'page title')

    def test_get_meta_description_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.page_de, 'meta_description'), None)

        # add page extensions
        AllinkTitleExtensionFactory(extended_object=self.page_de.get_title_obj())

        self.assertEqual(get_fallback(self.page_de, 'meta_description'), 'og description')

        self.page_de.get_title_obj().allinktitleextension.og_description = ''
        self.assertEqual(get_fallback(self.page_de, 'meta_description'), 'teaser description')

        self.page_de.get_title_obj().allinktitleextension.teaser_description = None
        self.assertEqual(get_fallback(self.page_de, 'meta_description'), None)

    def test_get_meta_image_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.page_de, 'meta_image'), self.allink_config.default_og_image)

        # add page extensions
        AllinkPageExtensionFactory(extended_object=self.page_de)

        self.assertEqual(get_fallback(self.page_de, 'meta_image'), self.page_de.allinkpageextension.og_image)

        self.page_de.allinkpageextension.og_image = None
        self.assertEqual(get_fallback(self.page_de, 'meta_image'), self.page_de.allinkpageextension.teaser_image)

        self.page_de.allinkpageextension.teaser_image = None
        self.assertEqual(get_fallback(self.page_de, 'meta_image'), self.allink_config.default_og_image)

    def test_get_meta_dict(self):

        expected_meta_context = {
            'meta_page_title': get_meta_page_title(self.page_de),
            'meta_title': get_fallback(self.page_de, 'meta_title'),
            'meta_description': get_fallback(self.page_de, 'meta_description'),
            'meta_image_url': getattr(get_fallback(self.page_de, 'meta_image'), 'url'),
            'google_site_verification': self.allink_config.google_site_verification,
        }
        self.assertDictEqual(expected_meta_context, get_page_meta_dict(self.page_de))


class AllinkExtensionTeaserTestCase(TestCase):

    def setUp(self):
        self.page_de = api.create_page(
            title='page title',
            template='default.html',
            language='de',
            published=True,
        )
        self.allink_config = ConfigFactory()

    def test_get_teaser_title_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.page_de, 'teaser_title'), 'page title')

        # add page extensions
        AllinkTitleExtensionFactory(extended_object=self.page_de.get_title_obj())

        self.assertEqual(get_fallback(self.page_de, 'teaser_title'), 'teaser title')

        self.page_de.get_title_obj().allinktitleextension.teaser_title = ''
        self.assertEqual(get_fallback(self.page_de, 'teaser_title'), 'page title')

    def test_get_teaser_description_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.page_de, 'teaser_description'), None)
        # add page extensions
        AllinkTitleExtensionFactory(extended_object=self.page_de.get_title_obj())

        self.assertEqual(get_fallback(self.page_de, 'teaser_description'), 'teaser description')

        self.page_de.get_title_obj().allinktitleextension.teaser_description = ''
        self.assertEqual(get_fallback(self.page_de, 'teaser_description'), None)

    def test_get_teaser_technical_title_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.page_de, 'teaser_technical_title'), None)

        # add page extensions
        AllinkTitleExtensionFactory(extended_object=self.page_de.get_title_obj())

        self.assertEqual(get_fallback(self.page_de, 'teaser_technical_title'), 'teaser technical title')

        self.page_de.get_title_obj().allinktitleextension.teaser_technical_title = ''
        self.assertEqual(get_fallback(self.page_de, 'teaser_technical_title'), None)

    def test_get_teaser_link_text_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.page_de, 'teaser_link_text'), 'Read more')

        # add page extensions
        AllinkTitleExtensionFactory(extended_object=self.page_de.get_title_obj())

        self.assertEqual(get_fallback(self.page_de, 'teaser_link_text'), 'teaser link text')

    def test_get_teaser_image_with_appropriate_fallbacks(self):
        self.assertEqual(get_fallback(self.page_de, 'teaser_image'), None)

        # add page extensions
        AllinkPageExtensionFactory(extended_object=self.page_de)

        self.assertEqual(get_fallback(self.page_de, 'teaser_image'), self.page_de.allinkpageextension.teaser_image)

        self.page_de.allinkpageextension.teaser_image = None
        self.assertEqual(get_fallback(self.page_de, 'teaser_image'), None)

    def test_get_teaser_dict(self):
        AllinkPageExtensionFactory(extended_object=self.page_de)

        expected_meta_context = {
            'teaser_title': get_fallback(self.page_de, 'teaser_title'),
            'teaser_technical_title': get_fallback(self.page_de, 'teaser_technical_title'),
            'teaser_description': get_fallback(self.page_de, 'teaser_description'),
            'teaser_image': get_fallback(self.page_de, 'teaser_image'),
            'teaser_link_text': get_fallback(self.page_de, 'teaser_link_text'),
            'teaser_link': self.page_de.get_absolute_url(),
        }
        self.assertDictEqual(expected_meta_context, get_page_teaser_dict(self.page_de))

# class AllinkUtilsTestCase(TestCase):
#
#     def setUp(self):
#         self.page_de = api.create_page(
#             title='page title',
#             template='default.html',
#             language='de',
#             published=True,
#         )
#
#     def test_get_fallback_invalid_key(self):
#         get_fallback()

