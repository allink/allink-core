# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TestCase

from allink_core.core_apps.allink_categories.tests import CategoryTestCaseMixin
from allink_core.core_apps.allink_categories.models import AllinkCategory as Category


class AdminTest(CategoryTestCaseMixin, TestCase):

    def test_admin_owner_default(self):
        """
        Test that the ChangeForm contains Treebeard's MoveNodeForm
        """
        from django.contrib import admin
        admin.autodiscover()

        user = self.create_user()
        user.is_superuser = True
        user.save()

        root = Category.add_root(name="test root")
        root.save()
        root = self.reload(root)
        root.add_child(name="test child 1")
        root.add_child(name="test child 2")

        admin_inst = admin.site._registry[Category]

        request = self.get_request('en')
        request.user = user
        request.META['HTTP_HOST'] = 'example.com'
        response = admin_inst.add_view(request)
        option = '<option value="first-child">First child of</option>'
        self.assertContains(response, option)
