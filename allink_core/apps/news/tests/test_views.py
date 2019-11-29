import json
from django.urls import reverse
from cms.test_utils.testcases import CMSTestCase
from django.test.testcases import TestCase
from allink_core.core.test import CategoriesMixin, DataModelMixin, PageApphookMixin, AllinkAppContenPluginMixin
from ..cms_apps import NewsApphook
from ..models import News
from ..views import NewsPluginLoadMore
from ..cms_plugins import CMSNewsAppContentPlugin
from .factories import NewsFactory


class NewsDetailViewTestCase(DataModelMixin, PageApphookMixin, CMSTestCase):
    apphook = 'NewsApphook'
    namespace = 'news'
    page_template = 'default.html'
    apphook_object = NewsApphook
    data_model_factory = NewsFactory

    def setUp(self):
        super().setUp()
        self.admin_user = self.get_superuser()

    def test_detail_when_inactive_404(self):
        inactive_entry = NewsFactory(status=News.INACTIVE)
        detail_url = reverse('{0}:detail'.format(self.namespace), kwargs={'slug': inactive_entry.slug})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 404)

    def test_detail_when_inactive_and_staff_user_200(self):
        inactive_entry = NewsFactory(status=News.INACTIVE)
        detail_url = reverse('{0}:detail'.format(self.namespace), kwargs={'slug': inactive_entry.slug})
        with self.login_user_context(self.admin_user):
            response = self.client.get(detail_url)
            self.assertEqual(response.status_code, 200)

    def test_detail_when_active_200(self):
        detail_url = reverse('{0}:detail'.format(self.namespace), kwargs={'slug': self.entry_1.slug})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)

    # def test_detail_get_template_names(self):
        # TODO 'get_template_names' method is already pretty voodoo. We should make this more explicit.
        # template_names = NewsDetail().get_template_names()

    # def test_detail_when_ajax_call(self):


class NewsPluginLoadMoreViewTestCaseApp(CategoriesMixin, DataModelMixin, AllinkAppContenPluginMixin, TestCase):
    apphook = 'NewsApphook'
    namespace = 'news'
    page_template = 'default.html'
    plugin_class = CMSNewsAppContentPlugin
    apphook_object = NewsApphook
    data_model_factory = NewsFactory
    load_more_view = NewsPluginLoadMore

    def test_more_without_plugin_id(self):
        more_url = '{}'.format(reverse('{0}:more'.format(self.namespace), kwargs={'page': 1}))
        response = self.client.get(more_url)
        self.assertEqual(response.status_code, 404)

    def test_more_without_plugin_in_db(self):
        more_url = '{}?plugin_id={}'.format(reverse('{0}:more'.format(self.namespace), kwargs={'page': 1}), 100)
        response = self.client.get(more_url)
        self.assertEqual(response.status_code, 404)

    def test_more_with_plugin_id(self):
        more_url = '{}?plugin_id={}'.format(reverse('{0}:more'.format(self.namespace), kwargs={'page': 1}), self.plugin_model_instance.id)
        response = self.client.get(more_url)
        self.assertEqual(response.status_code, 200)

    # def test_set_category_id(self):
    #     """"""
    #     pass

    def test_contenty_type_is_json(self):
        more_url = '{}?plugin_id={}'.format(reverse('{0}:more'.format(self.namespace), kwargs={'page': 1}), self.plugin_model_instance.id)
        response = self.client.get(more_url)
        self.assertEqual(response['Content-Type'], 'application/json')

    def test_json_no_result_false(self):
        more_url = '{}?plugin_id={}'.format(reverse('{0}:more'.format(self.namespace), kwargs={'page': 1}), self.plugin_model_instance.id)
        response = self.client.get(more_url)
        self.assertEqual(json.loads(response.content).get('no_results'), False)

    def test_json_no_result_true(self):
        self.plugin_model_instance.categories.set([self.category_1,])
        self.plugin_model_instance.save()

        more_url = '{}?plugin_id={}'.format(reverse('{0}:more'.format(self.namespace), kwargs={'page': 1}), self.plugin_model_instance.id)
        response = self.client.get(more_url)
        self.assertEqual(json.loads(response.content).get('no_results'), True)

    def test_json_with_pagination_no_next_page_url(self):
        more_url = '{}?plugin_id={}'.format(reverse('{0}:more'.format(self.namespace), kwargs={'page': 1}), self.plugin_model_instance.id)
        response = self.client.get(more_url)
        self.assertIsNone(json.loads(response.content).get('next_page_url'))

    def test_json_with_pagination_no_next_page_url_last_page(self):
        self.plugin_model_instance.paginated_by = 2
        self.plugin_model_instance.pagination_type = self.plugin_model_instance.LOAD
        self.plugin_model_instance.save()

        more_url = '{}?plugin_id={}'.format(reverse('{0}:more'.format(self.namespace), kwargs={'page': 3}), self.plugin_model_instance.id)
        response = self.client.get(more_url)
        self.assertIsNone(json.loads(response.content).get('next_page_url'))

    def test_json_with_pagination_next_page_url(self):
        self.plugin_model_instance.paginated_by = 2
        self.plugin_model_instance.pagination_type = self.plugin_model_instance.LOAD
        self.plugin_model_instance.save()

        more_url = '{}?plugin_id={}'.format(reverse('{0}:more'.format(self.namespace), kwargs={'page': 1}), self.plugin_model_instance.id)
        response = self.client.get(more_url)
        next_page_url = '{}?plugin_id={}'.format(reverse('{0}:more'.format(self.namespace), kwargs={'page': 2}), self.plugin_model_instance.id)
        self.assertEqual(json.loads(response.content).get('next_page_url'), next_page_url)

    def test_rendered_html_class_appended(self):
        more_url = '{}?plugin_id={}'.format(reverse('{0}:more'.format(self.namespace), kwargs={'page': 1}), self.plugin_model_instance.id)
        response = self.client.get(more_url)
        self.assertEqual(json.loads(response.content).get('rendered_content').count('appended'), 5)

    def test_rendered_html_pagination_first_page(self):
        self.plugin_model_instance.paginated_by = 2
        self.plugin_model_instance.pagination_type = self.plugin_model_instance.LOAD
        self.plugin_model_instance.save()

        more_url = '{}?plugin_id={}'.format(reverse('{0}:more'.format(self.namespace), kwargs={'page': 1}), self.plugin_model_instance.id)
        response = self.client.get(more_url)
        self.assertEqual(json.loads(response.content).get('rendered_content').count('>news entry'), 2)

    def test_rendered_html_pagination_second_page(self):
        self.plugin_model_instance.paginated_by = 2
        self.plugin_model_instance.pagination_type = self.plugin_model_instance.LOAD
        self.plugin_model_instance.save()

        more_url = '{}?plugin_id={}'.format(reverse('{0}:more'.format(self.namespace), kwargs={'page': 2}), self.plugin_model_instance.id)
        response = self.client.get(more_url)
        self.assertEqual(json.loads(response.content).get('rendered_content').count('>news entry'), 2)

    def test_rendered_html_pagination_last_page(self):
        self.plugin_model_instance.paginated_by = 2
        self.plugin_model_instance.pagination_type = self.plugin_model_instance.LOAD
        self.plugin_model_instance.save()

        more_url = '{}?plugin_id={}'.format(reverse('{0}:more'.format(self.namespace), kwargs={'page': 3}), self.plugin_model_instance.id)
        response = self.client.get(more_url)
        self.assertEqual(json.loads(response.content).get('rendered_content').count('>news entry'), 1)

    def test_get_queryset_default_all(self):
        """ TODO: will be obsolete after refactoring, because tested on plugin model """
        load_more_view = self.get_load_more_view()

        queryset = load_more_view.get_queryset()
        self.assertEqual(queryset.count(), 5)

    def test_get_queryset_default_filtered_by_category(self):
        """ Load more with a specific category. Default queryset -> ?plugin_id=1&category=2 """
        self.entry_1.categories.set([self.category_1])
        self.entry_2.categories.set([self.category_1])
        self.entry_3.categories.set([self.category_2])

        load_more_view = self.get_load_more_view()
        load_more_view.category_id = self.category_2.id  # this would be set by GET['category] = 2 in get method.
        load_more_view.category = self.category_2  # this would be set by GET['category] = 2 in get method.

        queryset = load_more_view.get_queryset()
        self.assertEqual(queryset.count(), 1)

    def test_get_queryset_manual_entries(self):
        """ TODO: will be obsolete after refactoring, because tested on plugin model """
        self.plugin_model_instance.manual_entries.set([self.entry_1, self.entry_2])

        load_more_view = self.get_load_more_view()

        queryset = load_more_view.get_queryset()
        self.assertEqual(queryset.count(), 2)

    def test_get_queryset_manual_entries_filtered_by_category(self):
        """ Load more with a specific category. Entries are selected manually. -> ?plugin_id=1&category=2 """
        self.entry_1.categories.set([self.category_1])
        self.entry_2.categories.set([self.category_2])
        self.plugin_model_instance.manual_entries.set([self.entry_1, self.entry_2])

        load_more_view = self.get_load_more_view()
        load_more_view.category_id = self.category_2.id  # this would be set by GET['category] = 2 in get method.
        load_more_view.category = self.category_2  # this would be set by GET['category] = 2 in get method.

        queryset = load_more_view.get_queryset()
        self.assertEqual(queryset.count(), 1)

    def test_get_context_data_no_pagination(self):
        load_more_view = self.get_load_more_view()
        load_more_view.object_list = load_more_view.get_queryset() # this would be set in get method.

        context = load_more_view.get_context_data()
        self.assertIsNone(context['paginator'])
        self.assertIsNone(context['page_obj'])
        self.assertFalse(context['is_paginated'])
        self.assertEqual(context['object_list'].count(), 5)

    def test_get_context_data_with_pagination_load_more(self):
        self.plugin_model_instance.paginated_by = 2
        self.plugin_model_instance.pagination_type = self.plugin_model_instance.LOAD
        self.plugin_model_instance.save()

        load_more_view = self.get_load_more_view()
        load_more_view.kwargs = {'page': 1}
        load_more_view.object_list = load_more_view.get_queryset() # this would be set in get method.

        context = load_more_view.get_context_data()
        self.assertIsNotNone(context['paginator'])
        self.assertEqual(context['page_obj'].object_list.count(), 2)
        self.assertTrue(context['is_paginated'])
        self.assertEqual(context['object_list'].count(), 2)

    def test_get_context_data_with_pagination_load_rest_first_page(self):
        """
        We used a quiet hacky way to use the paginator to load all the remaining items on the second page.
        paginator and page_object are not set correctly. We let the wrong values here!

        For displaying the "Load All" Button we use all information on the queryset. This might be hacky, but works.

        With LOAD_REST we use .paginated_by from the plugin on the first page. The second page should display all the remaining items.
        !! This is still broken, but we never noticed, because this view is always called with page=2.
        """
        self.plugin_model_instance.paginated_by = 2
        self.plugin_model_instance.pagination_type = self.plugin_model_instance.LOAD_REST
        self.plugin_model_instance.save()

        load_more_view = self.get_load_more_view()
        load_more_view.kwargs = {'page': 1}
        load_more_view.object_list = load_more_view.get_queryset() # this would be set in get method.

        context = load_more_view.get_context_data()
        self.assertEqual(context['paginator'].num_pages, 3)  # this is actually wrong, should be 2, as we want all the entries on the second page
        self.assertEqual(context['page_obj'].object_list.count(), 1)  # this is actually wrong, should be 3, as we want all the entries on the second page
        self.assertTrue(context['is_paginated'])
        self.assertEqual(context['object_list'].count(), 3)

    def test_get_context_data_with_pagination_load_rest_second_page(self):
        """
        We used a quiet hacky way to use the paginator to load all the remaining items on the second page.
        paginator and page_object are not set correctly. We let the wrong values here!

        For displaying the "Load All" Button we use all information on the queryset. This might be hacky, but works.
        """
        self.plugin_model_instance.paginated_by = 2
        self.plugin_model_instance.pagination_type = self.plugin_model_instance.LOAD_REST
        self.plugin_model_instance.save()

        load_more_view = self.get_load_more_view()
        load_more_view.kwargs = {'page': 2}
        load_more_view.object_list = load_more_view.get_queryset() # this would be set in get method.

        context = load_more_view.get_context_data()
        self.assertEqual(context['paginator'].num_pages, 3)  # this is actually wrong, should be 2, as we want all the entries on the second page
        self.assertEqual(context['page_obj'].object_list.count(), 1)  # this is actually wrong, should be 3. but is now set to the actual last page of the original paginator where the count 1
        self.assertFalse(context['page_obj'].has_next())
        self.assertTrue(context['is_paginated'])
        self.assertEqual(context['object_list'].count(), 3)




