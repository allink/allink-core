import pickle
from django.test.testcases import TransactionTestCase, override_settings
from unittest.mock import patch, call
from django.conf import settings
from parler.utils.context import switch_language
from ..models import Config
from .factories import ConfigFactory



MEMCACHED_CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


class AllinkConfigTestCase(TransactionTestCase):

    def setUp(self):
        self.allink_config = ConfigFactory()

    def test_config_language_no_cache(self):
        for lang, _ in settings.LANGUAGES:
            with switch_language(self.allink_config, lang):
                self.assertEqual(self.allink_config.newsletter_signup_link, 'newsletter_signup_link_{}'.format(lang))

    def test_config_language_get_cache_key(self):
        for lang, _ in settings.LANGUAGES:
            with switch_language(self.allink_config, lang):
                self.assertEqual(self.allink_config.get_cache_key(lang), 'solo:config_{}'.format(lang))

    @patch('django.core.cache.cache.set')
    def test_config_language_set_to_cache(self, mock_cache_set):
        """
        every language will be set to cache, so for one language ('en') all languages (3) will be set to cache.
        checks also if correct translated object "allink_config" gets saved to cache
        """
        with switch_language(self.allink_config, 'en'):
            self.allink_config.set_to_cache()
            expected_calls = [call('solo:config_{}'.format('en'), pickle.dumps(self.allink_config), 15552000)]
            mock_cache_set.assert_has_calls(expected_calls)

            with switch_language(self.allink_config, 'de'):
                expected_calls = [call('solo:config_{}'.format('de'), pickle.dumps(self.allink_config), 15552000)]
                mock_cache_set.assert_has_calls(expected_calls)

            with switch_language(self.allink_config, 'fr'):
                expected_calls = [call('solo:config_{}'.format('fr'), pickle.dumps(self.allink_config), 15552000)]
                mock_cache_set.assert_has_calls(expected_calls)

        self.assertEqual(mock_cache_set.call_count, len(settings.LANGUAGES))  # for each language total: 3 times

    @patch('django.core.cache.cache.get')
    def test_get_solo(self, mock_cache_get):
        for lang, _ in settings.LANGUAGES:
            mock_cache_get.return_value = pickle.dumps(self.allink_config)
            with switch_language(self.allink_config, lang):
                self.assertEqual(self.allink_config, Config.get_solo())

    @override_settings(CACHES=MEMCACHED_CACHES)
    def test_get_solo_meme_cache_get_solo(self):
        with switch_language(self.allink_config, 'en'):
            self.allink_config.set_to_cache()
            self.assertEqual(self.allink_config, Config.get_solo())

            with switch_language(self.allink_config, 'de'):
                self.assertEqual(self.allink_config, Config.get_solo())

            with switch_language(self.allink_config, 'fr'):
                self.assertEqual(self.allink_config, Config.get_solo())

    @patch('django.core.cache.cache.get')
    def test_get_solo_not_cached(self, mock_cache_get):
        for lang, _ in settings.LANGUAGES:
            mock_cache_get.return_value = None
            with switch_language(self.allink_config, lang):
                self.assertEqual(self.allink_config, Config.get_solo())

    @patch('cms.cache.invalidate_cms_page_cache')
    @patch('django.core.cache.cache.clear')
    @patch('menus.menu_pool.menu_pool.clear')
    def test_save_invalidate_cms_page_cache(self, mock_menu_pool_clear, mock_cache_clear, mock_invalidate_cms_page_cache):
        self.allink_config.save()
        mock_invalidate_cms_page_cache.assert_called_once()
        mock_cache_clear.assert_called_once()
        mock_menu_pool_clear.assert_called_once()
