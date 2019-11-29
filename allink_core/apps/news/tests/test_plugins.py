from django.test.client import RequestFactory
from django.test.testcases import TestCase
from allink_core.core.test import CategoriesMixin, DataModelMixin, AllinkAppContenPluginMixin
from allink_core.apps.news.cms_apps import NewsApphook
from .factories import NewsFactory
from ..cms_plugins import CMSNewsAppContentPlugin


class CMSNewsAppContentPluginTestCaseApp(CategoriesMixin, DataModelMixin, AllinkAppContenPluginMixin, TestCase):
    apphook = 'NewsApphook'
    namespace = 'news'
    page_template = 'default.html'
    apphook_object = NewsApphook
    data_model_factory = NewsFactory
    plugin_class = CMSNewsAppContentPlugin

    def test_context_object_list_all(self):
        plugin_instance = self.plugin_model_instance.get_plugin_class_instance()
        context = {'request': RequestFactory()}
        context = plugin_instance.render(context, self.plugin_model_instance, None)
        self.assertEqual(context['object_list'].count(), 5)
        self.assertNotIn('page_obj', context)
        self.assertNotIn('next_page_url', context)

    def test_context_object_list_manual_entries(self):
        """ TODO: will be obsolete after refactoring, because tested on plugin model """
        plugin_instance = self.plugin_model_instance.get_plugin_class_instance()
        self.plugin_model_instance.manual_entries.set([self.entry_1, self.entry_2])
        context = {'request': RequestFactory()}
        context = plugin_instance.render(context, self.plugin_model_instance, None)
        self.assertEqual(context['object_list'].count(), 2)
        self.assertNotIn('page_obj', context)
        self.assertNotIn('next_page_url', context)

    def test_context_object_list_category_navigation_enabled(self):
        """ TODO: will be obsolete after refactoring, because tested on plugin model """
        self.plugin_model_instance.categories.set([self.category_1, self.category_2,])
        plugin_instance = self.plugin_model_instance.get_plugin_class_instance()
        self.entry_1.categories.set([self.category_1,])
        self.entry_2.categories.set([self.category_1,])
        self.entry_3.categories.set([self.category_1,])
        self.entry_4.categories.set([self.category_2, ])
        self.plugin_model_instance.category_navigation_enabled = True

        context = {'request': RequestFactory()}
        context = plugin_instance.render(context, self.plugin_model_instance, None)
        self.assertEqual(context['object_list'].count(), 3)
        self.assertNotIn('page_obj', context)
        self.assertNotIn('next_page_url', context)

    def test_context_pagination(self):
        self.plugin_model_instance.paginated_by = 2
        self.plugin_model_instance.pagination_type = self.plugin_model_instance.LOAD

        plugin_instance = self.plugin_model_instance.get_plugin_class_instance()
        context = {'request': RequestFactory()}

        context = plugin_instance.render(context, self.plugin_model_instance, None)
        self.assertEqual(context['object_list'].count(), 2)
        self.assertIn('page_obj', context)
        self.assertIn('next_page_url', context)

    def test_context_pagination_no_next_page(self):
        self.plugin_model_instance.paginated_by = 5
        self.plugin_model_instance.pagination_type = self.plugin_model_instance.LOAD

        plugin_instance = self.plugin_model_instance.get_plugin_class_instance()
        context = {'request': RequestFactory()}

        context = plugin_instance.render(context, self.plugin_model_instance, None)
        self.assertEqual(context['object_list'].count(), 5)
        self.assertNotIn('page_obj', context)
        self.assertNotIn('next_page_url', context)

    def test_context_category_navigation(self):
        self.plugin_model_instance.category_navigation_enabled = True

        plugin_instance = self.plugin_model_instance.get_plugin_class_instance()
        context = {'request': RequestFactory()}

        context = plugin_instance.render(context, self.plugin_model_instance, None)
        self.assertIn('category_navigation', context)
        self.assertIn('by_category', context)

    def test_context_category_navigation_next_page_url_with_manual_entries(self):
        """
        Special case, where we want to have a category navigation (without the tab "All") on manual_entries with a Load More Button.
        """
        self.plugin_model_instance.category_navigation_enabled = True
        self.plugin_model_instance.manual_entries.set([self.entry_1, self.entry_2, self.entry_3])
        self.plugin_model_instance.paginated_by = 2
        self.plugin_model_instance.pagination_type = self.plugin_model_instance.LOAD

        self.entry_1.categories.set([self.category_1,])
        self.entry_2.categories.set([self.category_1,])
        self.entry_3.categories.set([self.category_1,])
        self.entry_4.categories.set([self.category_2, ])

        plugin_instance = self.plugin_model_instance.get_plugin_class_instance()
        context = {'request': RequestFactory()}
        context = plugin_instance.render(context, self.plugin_model_instance, None)
        self.assertIn('next_page_url', context)

    def test_get_render_template_no_result(self):
        plugin_instance = self.plugin_model_instance.get_plugin_class_instance()
        context = {'request': RequestFactory(), 'object_list': []}

        render_template = plugin_instance.get_render_template(context, self.plugin_model_instance, None)
        self.assertIn('no_results.html', render_template)

    def test_get_render_template_results(self):
        plugin_instance = self.plugin_model_instance.get_plugin_class_instance()
        context = {'request': RequestFactory(), 'object_list': [self.entry_1]}

        render_template = plugin_instance.get_render_template(context, self.plugin_model_instance, None)
        self.assertNotIn('no_results.html', render_template)




