import tempfile
import hashlib
import os
from django.test import TestCase
from ..utils import copy_dummy_dir, create_new_app, rename_dummy_classes


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class CustomisationNewAppTestCase(TestCase):
    dummy_path = 'allink_core/core/customisation/dummy_app'
    app_label = 'new_app'
    model_name = 'NewApp'

    expected_dirs = [
        'cms_plugins.py',
        'managers.py',
        'urls.py',
        'sitemaps.py',
        'templates',
        'cms_toolbars.py',
        'README.md',
        'tests',
        'views.py',
        '__init__.py',
        'models.py',
        'cms_apps.py',
        'admin.py',
        'config.py'
    ]

    expected_tests = [
        'test_admin.py',
        'test_models.py',
        '__init_.py',
        'test_views.py',
        'test_managers.py',
        'test_plugins.py',
        'factories.py'
    ]

    expected_templates = [
        'dummyapp_detail.html',
        'plugins'
    ]

    def test_copy_dummy_dir_already_exists(self):
        apps_dir = 'apps'
        with self.assertRaisesRegex(OSError, "'{}' directory already exists!".format(apps_dir)):
            copy_dummy_dir(dummy_path=self.dummy_path, app_path=apps_dir)

    def test_copy_dummy_dir_all_files_copied(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_dir = os.path.join(temp_apps_dir, self.app_label)
            copy_dummy_dir(dummy_path=self.dummy_path, app_path=full_temp_dir)

            # app root dir
            self.assertCountEqual(self.expected_dirs, os.listdir(full_temp_dir))

            # app tests dir
            tests_dir = os.path.join(full_temp_dir, 'tests')
            self.assertCountEqual(self.expected_tests, os.listdir(tests_dir))

            # app templates dir
            template_dir = os.path.join(full_temp_dir, 'templates', 'dummy_app')
            self.assertCountEqual(self.expected_templates, os.listdir(template_dir))

    def test_rename_dummy_classes_in_one_file(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_dir = os.path.join(temp_apps_dir, self.app_label)
            copy_dummy_dir(dummy_path=self.dummy_path, app_path=full_temp_dir)

            new_file = os.path.join(full_temp_dir, 'models.py')

            replace = {
                'dummy_app': self.app_label,
                'DummyApp': self.model_name,
                'dummy-app': 'new-app',
            }

            rename_dummy_classes(new_file, replace)

            with open(new_file) as f:
                s = f.read()
                self.assertIn('class NewApp(', s)
                self.assertIn('from .managers import NewAppManager', s)
                self.assertIn('new_app.NewApp', s)
                self.assertNotIn('dummy_app', s)
                self.assertNotIn('DummyApp', s)

    def test_create_new_app_all_files_copied_no_readme(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_dir = os.path.join(temp_apps_dir, self.app_label)
            create_new_app(dummy_path=self.dummy_path, app_path=temp_apps_dir, app_label=self.app_label, model_name=self.model_name)

            # no README.md
            expected_dirs = self.expected_dirs
            expected_dirs.remove('README.md')
            self.assertListEqual(expected_dirs, os.listdir(full_temp_dir))
