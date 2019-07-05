from django.test import TransactionTestCase, Client
from django.contrib import admin

from cms.utils.urlutils import admin_reverse

from ..models import News
from ..cms_apps import NewsApphook
from ..admin import NewsAdmin
from .factories import NewsFactory

from allink_core.core.test.factories import (
    UserFactory
)

from allink_core.core.test import DefaultApphookTestCase

from cms.api import create_page, create_title
from cms.utils.i18n import force_language



class NewsAdminTestCase(DefaultApphookTestCase):

    apphook = 'NewsApphook'
    namespace = 'news'
    template = 'default.html'

    apphook_object = NewsApphook


    def setUp(self):
        super().setUp()

        self.admin_user = self.get_superuser()
        self.entry_1 = NewsFactory()
        self.model_admin_1 = NewsAdmin(self.entry_1, admin.site)

    def test_all_languages_column(self):
        # Check that all the available languages appear in `all_translations`
        all_translations = self.model_admin_1.all_languages_column(self.entry_1)

        change_url = admin_reverse('news_news_change', args=[self.entry_1.id])

        self.assertTrue(change_url + '?language=en' in all_translations)
        self.assertTrue(change_url + '?language=de' in all_translations)
        self.assertTrue(change_url + '?language=fr' in all_translations)

    def test_change_list_view(self):
        with self.login_user_context(self.admin_user):
            response = self.client.get(admin_reverse('news_news_changelist'))
            self.assertEqual(response.status_code, 200)

    def test_change_view(self):
        with self.login_user_context(self.admin_user):
            response = self.client.get(admin_reverse('news_news_change', args=[self.entry_1.id]))
            self.assertEqual(response.status_code, 200)
