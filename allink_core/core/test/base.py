import sys
from django.conf import settings
from django.core.cache import cache
from django.urls import clear_url_caches
from cms.apphook_pool import apphook_pool
from cms.appresolver import clear_app_resolvers

from cms import api
from cms.exceptions import AppAlreadyRegistered
from cms.test_utils.testcases import TransactionCMSTestCase


__all__ = [
    'CleanUpMixin',
    'DefaultApphookTestCase'
]


class CleanUpMixin:
    """
    Creates the default app hook page.

    e.g
    apphook_object = NewsApphook
    """

    apphook_object = None

    def setUp(self):
        super().setUp()
        apphook_object = self.get_apphook_object()
        self.reload_urls(apphook_object)

    def tearDown(self):
        """
        Do a proper cleanup, delete everything what is preventing us from
        clean environment for tests.
        :return: None
        """
        self.reset_all()
        cache.clear()
        super(CleanUpMixin, self).tearDown()

    def get_apphook_object(self):
        return self.apphook_object

    def reset_all(self):
        """
        Reset all that could leak from previous test to current/next test.
        :return: None
        """
        apphook_object = self.get_apphook_object()
        self.delete_app_module(apphook_object.__module__)
        self.reload_urls(apphook_object)
        self.apphook_clear()

    def delete_app_module(self, app_module=None):
        """
        Remove APP_MODULE from sys.modules. Taken from cms.
        :return: None
        """
        if app_module is None:
            apphook_object = self.get_apphook_object()
            app_module = getattr(apphook_object, '__module__')
        if app_module in sys.modules:
            del sys.modules[app_module]

    def apphook_clear(self):
        """
        Clean up apphook_pool and sys.modules. Taken from cms with slight
        adjustments and fixes.
        :return: None
        """
        try:
            apphooks = apphook_pool.get_apphooks()
        except AppAlreadyRegistered:
            # there is an issue with discover apps, or i'm using it wrong.
            # setting discovered to True solves it. Maybe that is due to import
            # from aldryn_events.cms_apps which registers EventListAppHook
            apphook_pool.discovered = True
            apphooks = apphook_pool.get_apphooks()

        for name, label in list(apphooks):
            if apphook_pool.apps[name].__class__.__module__ in sys.modules:
                del sys.modules[apphook_pool.apps[name].__class__.__module__]
        apphook_pool.clear()

    def reload_urls(self, apphook_object=None):
        """
        Clean up url related things (caches, app resolvers, modules).
        Taken from cms.
        :return: None
        """
        if apphook_object is None:
            apphook_object = self.get_apphook_object()
        app_module = apphook_object.__module__
        package = app_module.split('.')[0]
        clear_app_resolvers()
        clear_url_caches()
        url_modules = [
            'cms.urls',
            '{0}.urls'.format(package),
            settings.ROOT_URLCONF
        ]

        for module in url_modules:
            if module in sys.modules:
                del sys.modules[module]


class DefaultApphookTestCase(CleanUpMixin, TransactionCMSTestCase):
    """
    Creates the default app hook page.

    e.g
    apphook = 'NewsApphook'
    namespace = 'news'
    template = 'default.html'
    """

    apphook = None
    namespace = None
    template = None

    def setUp(self):
        super().setUp()
        self.language = settings.LANGUAGES[0][0]

        self.root_page = api.create_page(
            title='root_page',
            template=self.template,
            language=self.language,
            published=True,
        )
        try:
            # Django-cms 3.5 doesn't set is_home when create_page is called
            self.root_page.set_as_homepage()
        except AttributeError:
            pass

        self.page = api.create_page(
            title='page',
            template=self.template,
            language=self.language,
            published=True,
            parent=self.root_page,
            apphook=self.apphook,
            apphook_namespace=self.namespace
        )
        self.plugin_page = api.create_page(
            title="plugin_page",
            template=self.template,
            language=self.language,
            parent=self.root_page,
            published=True
        )

        # self.placeholder = self.page.placeholders.all()[0]
        # self.setup_categories()

        # translated and publish all created pages
        for page in self.root_page, self.page, self.plugin_page:
            for language, _ in settings.LANGUAGES[1:]:
                api.create_title(language, '{}: {}'.format(page.get_slug(), language), page)
                page.publish(language)
                page.set_translations_cache()
