# -*- coding: utf-8 -*-

from django.test import TransactionTestCase, override_settings
from django.utils.translation import override, force_text

from allink_core.core_apps.allink_categories.models import AllinkCategory

from allink_core.apps.work.tests import DefaultSetupMixin, DefaultApphookMixin, CleanUpMixin, BaseWorkTest

from allink_core.core.loading import get_model
Work = get_model('work', 'Work')


class TestBasicWorkModels(DefaultSetupMixin, DefaultApphookMixin, CleanUpMixin, TransactionTestCase):

    def setUp(self):
        super(TestBasicWorkModels, self).setUp()
        # get some time to reload urls
        self.client.get(self.app_hook_page.get_absolute_url())

    def test_create_work(self):
        """We can create a work with a title."""
        title = 'Work Test 1'
        work = Work.objects.create(title=title)
        self.assertEqual(work.title, title)
        self.assertEqual(Work.objects.all()[0], work)

    def test_delete_work(self):
        """We can delete a work."""
        title = 'Work Delete'
        work = Work.objects.create(title=title)
        Work.objects.get(pk=work.pk).delete()
        self.assertFalse(Work.objects.filter(pk=work.pk))

    def test_str(self):
        title = 'Work Str'
        work = Work.objects.create(title=title)
        created_str = work.created.strftime('%d.%m.%Y')
        self.assertEqual(force_text(work), title + ' - ' + created_str)

    def test_absolute_url(self):
        slug = 'work-slug'
        work = Work.objects.create(slug=slug)
        # This isn't a translation test, per se, but let's make sure that we
        # have a predictable language prefix, regardless of the tester's locale.
        with override('en'):
            app_hook_url = self.app_hook_page.get_absolute_url()
            self.assertEqual(
                work.get_absolute_url(),
                '{0}{1}/'.format(app_hook_url, slug)
            )

    def test_auto_slugify(self):
        title = 'Project Test with Hans'
        slug = 'project-test-with-hans'
        work = Work.objects.create(title=title)
        work.save()
        self.assertEquals(work.slug, slug)

    def test_auto_slugify_same_title(self):
        title_1 = 'Project Test with Hans'
        slug_1 = 'project-test-with-hans'
        work_1 = Work.objects.create(title=title_1)
        work_1.save()

        title_2 = 'Project Test with Hans'
        slug_2 = 'project-test-with-hans-1'
        work_2 = Work.objects.create(title=title_2)
        work_2.save()

        self.assertEquals(work_1.slug, slug_1)
        self.assertEquals(work_2.slug, slug_2)


class TestWorkModelTranslation(BaseWorkTest):

    def test_work_translatable(self):
        work1 = self.reload(self.work1, 'en')
        self.assertEqual(
            work1.title,
            self.data['work1']['en']['title']
        )
        work1 = self.reload(self.work1, 'de')
        self.assertEqual(
            work1.safe_translation_getter('title'),
            self.data['work1']['de']['title']
        )

    def test_lead(self):
        work1 = self.reload(self.work1, 'en')
        self.assertEqual(
            work1.lead,
            self.data['work1']['en']['lead']
        )
        work1 = self.reload(self.work1, 'de')
        self.assertEqual(
            work1.lead,
            self.data['work1']['de']['lead']
        )


class TestWorkModelCategories(BaseWorkTest):

    def test_get_relevant_categories(self):
        """
        work is tagged with only one category
        two root categories with tottaly 3 relevant category for model_name "work"
        """
        work1 = self.reload(self.work1, 'en')
        work1.categories.add(self.category1)
        category1 = self.reload(self.category1)
        category2 = self.reload(self.category2)
        category3 = self.reload(self.category3)
        # categories has only one defined category
        self.assertListEqual(
            list(work1.get_relevant_categories()),
            [category1, category2, category3]
        )

    def test_get_relevant_categories_multiple_categories(self):
        """
        work is tagged with two categories
        two root categories with each a relevant category for model_name "work"
        one root categories with a relevant category for model_name "people"
        """
        work1 = self.reload(self.work1, 'en')
        work1.categories.add(self.category1)
        work1.categories.add(self.category3)
        category1 = self.reload(self.category1)
        category2 = self.reload(self.category2)
        category3 = self.reload(self.category3)
        self.assertListEqual(
            list(work1.get_relevant_categories()),
            [category1, category2, category3]
        )

    @override_settings(PROJECT_APP_MODEL_CATEGORY_TAG_CHOICES=[('work', 'Work'), ])
    def test_auto_create_category(self):
        work1 = Work.objects.create(title='Test Work with category')
        work1.save()

        cat1 = AllinkCategory.objects.get(id=work1.auto_generated_category.id)
        self.assertEquals(work1.auto_generated_category, cat1)\

    @override_settings(PROJECT_APP_MODEL_CATEGORY_TAG_CHOICES=[])
    def test_auto_not_create_category(self):
        work1 = Work.objects.create(title='Test Work with category')
        work1.save()
        temp_cat_count = AllinkCategory.objects.all().count()

        self.assertEquals(work1.auto_generated_category, None)
        # no category has been created
        self.assertEquals(AllinkCategory.objects.all().count(), temp_cat_count)
