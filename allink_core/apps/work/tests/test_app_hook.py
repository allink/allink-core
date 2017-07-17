# # -*- coding: utf-8 -*-
#
# from __future__ import unicode_literals
#
# from django.core.urlresolvers import reverse
# from cms.apphook_pool import apphook_pool
#
# from ..models import Work
#
# from . import BaseWorkTest
#
#
# class TestWorkAppHook(BaseWorkTest):
#
#     def test_add_work_app(self):
#         """
#         We add a work to the app
#         """
#         self.page.application_urls = 'WorkApp'
#         self.page.application_namespace = 'work'
#         self.page.publish(self.language)
#
#         work = Work.objects.create(
#             title='Project Example', lead='Test Lorem',
#             slug='project-example'
#         )
#         # By slug
#         url = reverse(
#             'work:detail', kwargs={'slug': work.slug})
#         response = self.client.get(url)
#         self.assertContains(response, 'Project Example')
