# # -*- coding: utf-8 -*-
#

"""
AllinkBasePluginLoadMoreView is going to bes testet in test_plugins.py
"""

# from __future__ import unicode_literals
#
# from django.core.urlresolvers import reverse
# from django.http import Http404
# from django.test.client import RequestFactory
#
# from cms.utils.i18n import force_language
#
#
# from . import DefaultApphookMixin, BaseWorkTest, CMSRequestBasedTest
#
#
# class TestMainListView(BaseWorkTest, CMSRequestBasedTest):
#
#     def test_list_view_with_only_en_apphook(self):
#         page = self.create_apphook_page(multilang=False)
#         # give some time for apphook reload middleware
#         self.client.get(page.get_absolute_url())
#
#         self.set_default_work_objects_current_language('en')
#         with force_language('en'):
#             url = page.get_absolute_url()
#             work1_url = self.work1.get_absolute_url()
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, self.work1.title)
#         self.assertContains(response, work1_url)
#         # should not contain person 2 since page for 'de' language is
#         # not published
#         self.assertNotContains(response, self.work2.title)
#         self.assertNotContains(response, self.work2.slug)
#
#     def test_list_view_with_en_and_de_apphook(self):
#         page = self.create_apphook_page(multilang=True)
#         # give some time for apphook reload middleware
#         self.client.get(page.get_absolute_url())
#         self.set_default_work_objects_current_language('en')
#         with force_language('en'):
#             url = page.get_absolute_url()
#             work1_url = self.work1.get_absolute_url()
#             work2_url = self.work2.get_absolute_url()
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, self.work1.title)
#         self.assertContains(response, self.work2.title)
#         self.assertContains(response, work1_url)
#         self.assertContains(response, work2_url)
