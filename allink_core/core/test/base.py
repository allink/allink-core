import sys
import random
import string
from django.utils.translation import override
from django.conf import settings
from django.core.cache import cache
from django.urls import clear_url_caches
from django.test.client import RequestFactory
from parler.utils.context import switch_language
from cms.apphook_pool import apphook_pool
from cms.appresolver import clear_app_resolvers
from cms import api
from cms.exceptions import AppAlreadyRegistered
from allink_core.core_apps.allink_categories.models import AllinkCategory

__all__ = [
    'PageApphookMixin',
    'CategoriesMixin',
    'DataModelMixin',
    'DataModelTranslationMixin',
    'PluginModelMixin',
]


class PageApphookMixin:
    """
    Creates the following objects:

    root_page
    page
    plugin_page
    placeholder

    Cleans up cache and a bunch of cms related stuff.

    usage example attributes:

    apphook_object = NewsApphook
    apphook = 'NewsApphook'
    namespace = 'news'
    page_template = 'default.html'

    """
    apphook_object = None
    apphook = None
    namespace = None
    page_template = None

    def setUp(self):
        super().setUp()
        self.language = settings.LANGUAGES[0][0]
        apphook_object = self.get_apphook_object()
        self.reload_urls(apphook_object)

        self.root_page = api.create_page(
            title='root_page',
            template=self.page_template,
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
            template=self.page_template,
            language=self.language,
            published=True,
            parent=self.root_page,
            apphook=self.apphook,
            apphook_namespace=self.namespace
        )
        self.plugin_page = api.create_page(
            title="plugin_page",
            template=self.page_template,
            language=self.language,
            parent=self.root_page,
            published=True
        )

        self.placeholder = self.page.placeholders.all()[0]

        # translated and publish all created pages
        for page in self.root_page, self.page, self.plugin_page:
            for language, _ in settings.LANGUAGES[1:]:
                api.create_title(language, '{}: {}'.format(page.get_slug(), language), page)
                page.publish(language)
                page.set_translations_cache()

    def tearDown(self):
        """
        Do a proper cleanup, delete everything what is preventing us from
        clean environment for tests.
        :return: None
        """
        self.reset_all()
        cache.clear()
        super(PageApphookMixin, self).tearDown()

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


class CategoriesMixin:
    """
    Creates the following objects and its translation:

    category_root
    category_1
    category_2

    """

    def setUp(self):
        super().setUp()
        self.setup_categories()

    @staticmethod
    def reload(node):
        """NOTE: django-treebeard requires nodes to be reloaded via the Django
        ORM once its sub-tree is modified for the API to work properly.
        See:: https://tabo.pe/projects/django-treebeard/docs/2.0/caveats.html
        This is a simple helper-method to do that."""
        return node.__class__.objects.get(id=node.id)

    @classmethod
    def rand_str(cls, prefix=u'', length=23, chars=string.ascii_letters):
        return prefix + u''.join(random.choice(chars) for _ in range(length))

    def setup_categories(self):
        """
        Sets-up i18n categories (self.category_root, self.category_1 and
        self.category_2) for use in tests
        """
        self.language = settings.LANGUAGES[0][0]

        categories = []
        # Set the default language, create the objects
        with override(self.language):
            code = "{0}-".format(self.language)
            self.category_root = AllinkCategory.add_root(
                name=self.rand_str(prefix=code, length=8))
            categories.append(self.category_root)
            self.category_1 = self.category_root.add_child(
                name=self.rand_str(prefix=code, length=8))
            categories.append(self.category_1)
            self.category_2 = self.category_root.add_child(
                name=self.rand_str(prefix=code, length=8))
            categories.append(self.category_2)

        # We should reload category_root, since we modified its children.
        self.category_root = self.reload(self.category_root)

        # Setup the other language(s) translations for the categories
        for language, _ in settings.LANGUAGES[1:]:
            for category in categories:
                with switch_language(category, language):
                    code = "{0}-".format(language)
                    category.name = self.rand_str(prefix=code, length=8)
                    category.save()


class DataModelMixin:
    """
    Creates the following objects:

    allink_config
    entry_1
    entry_2
    entry_3
    entry_4
    entry_5

    usage example attributes:

    data_model_factory = NewsFactory

    """
    data_model_factory = None

    def setUp(self):
        from allink_core.apps.config.tests.factories import ConfigFactory
        super().setUp()
        self.allink_config = ConfigFactory()
        self.entry_1 = self.data_model_factory()
        self.entry_2 = self.data_model_factory()
        self.entry_3 = self.data_model_factory()
        self.entry_4 = self.data_model_factory()
        self.entry_5 = self.data_model_factory()


class DataModelTranslationMixin:
    """
    Creates the translations in languages de and fr for the following objects:

    relies on DataModelMixin!

    entry_1
    entry_2
    entry_3
    entry_4
    entry_5

    """

    def setUp(self):
        super().setUp()
        entries = [self.entry_1, self.entry_2, self.entry_3, self.entry_4, self.entry_5]

        # Setup the other language(s) translations for the entries
        for language, _ in settings.LANGUAGES[1:]:
            for entry in entries:
                title = '{}-{}'.format(entry.title, language)
                with switch_language(entry, language):
                    entry.title = title
                    entry.save()


class PluginModelMixin(PageApphookMixin):
    """
    Creates the following objects:

    placeholder
    plugin_model_instance

    usage example attributes:

    plugin_class = CMSNewsAppContentPlugin
    load_more_view = NewsPluginLoadMore

    """
    plugin_class = None
    load_more_view = None

    def setUp(self):
        super().setUp()
        self.placeholder = self.plugin_page.placeholders.all()[0]
        self.plugin_model_instance = api.add_plugin(
            self.placeholder,
            self.plugin_class,
            self.language,
            # allink default values
            template='grid_static',
        )

    def get_load_more_view(self):
        """ returns a pseudo instantiated load_more_view """
        load_more_view = self.load_more_view()
        load_more_view.plugin = self.plugin_model_instance
        load_more_view.request = RequestFactory()
        load_more_view.request.GET = {}
        return load_more_view
