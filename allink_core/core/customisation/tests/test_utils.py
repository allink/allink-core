import tempfile
import os
from django.test import TestCase
from unittest import mock
from distutils.errors import DistutilsFileError
from ..utils import get_path, copy_dir, create_new_app, replace_strings, rename, fork_allink_app


class CustomisationUtilsTestCase(TestCase):
    dummy_app_path = 'allink_core/core/customisation/dummy_new_app'
    app_label = 'new_app'
    model_name = 'NewApp'

    def test_get_path_from_module(self):
        import django
        django_dirname = os.path.dirname(django.db.models.__file__)
        path_from_module_string = get_path('django.db.models')

        self.assertEqual(path_from_module_string, django_dirname)

    def test_get_path_from_module_not_found(self):
        with self.assertRaisesRegex(ModuleNotFoundError, "No module named 'some_model'"):
            get_path('some_model.something')

    def test_copy_dummy_dir_already_exists(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            apps_dir = temp_apps_dir
            with self.assertRaisesRegex(OSError, "'{}' directory already exists!".format(apps_dir)):
                copy_dir(dummy_app=self.dummy_app_path, app_path=apps_dir)

    def test_copy_dummy_dir_wrong_dummy_path(self):
        wrong_dummy_path = 'hello'
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            apps_dir = os.path.join(temp_apps_dir, self.app_label)
            with self.assertRaisesRegex(DistutilsFileError, "cannot copy tree '{}': not a directory".format(wrong_dummy_path)):
                copy_dir(dummy_app=wrong_dummy_path, app_path=apps_dir)

    def test_copy_dummy_dir_all_files_copied(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)
            copy_dir(dummy_app=self.dummy_app_path, app_path=full_temp_path)
            total_file_count = sum([len(files) for r, d, files in os.walk(full_temp_path)])
            expected_file_count = 23
            self.assertEqual(total_file_count, expected_file_count)

    def test_rename_dummy_classes_in_one_file(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)
            copy_dir(dummy_app=self.dummy_app_path, app_path=full_temp_path)

            new_file = os.path.join(full_temp_path, 'models.py')

            replace = {
                'dummy_app': self.app_label,
                'DummyApp': self.model_name,
                'dummy-app': 'new-app',
            }

            replace_strings(new_file, replace)

            # test some strings which should be in this file
            with open(new_file) as f:
                s = f.read()
                self.assertIn('class NewApp(', s)
                self.assertIn('from .managers import NewAppManager', s)
                self.assertIn('new_app.NewApp', s)
                self.assertNotIn('dummy_app', s)
                self.assertNotIn('DummyApp', s)

    def test_rename_dir_or_file_one_file(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)
            copy_dir(dummy_app=self.dummy_app_path, app_path=full_temp_path)

            replace = {
                'dummy_app': self.app_label,
                'dummyapp': self.model_name.lower(),
            }
            # file
            new_file = os.path.join(full_temp_path, 'templates', 'dummy_app', 'dummyapp_detail.html')
            rename(path=new_file, replace=replace)
            renamed_file = os.path.join(full_temp_path, 'templates', 'dummy_app', 'newapp_detail.html')
            self.assertTrue(os.path.isfile(renamed_file))

            # dir
            new_dir = os.path.join(full_temp_path, 'templates', 'dummy_app')
            rename(path=new_dir, replace=replace)
            renamed_dir = os.path.join(full_temp_path, 'templates', 'new_app')
            self.assertTrue(os.path.isdir(renamed_dir))


class CustomisationNewAppTestCase(TestCase):
    dummy_app = 'allink_core.core.customisation.dummy_new_app'
    app_label = 'new_app'
    model_name = 'NewApp'

    @mock.patch('allink_core.core.customisation.utils.replace_strings')
    def test_create_new_app_all_files_string_replaced(self, mock_replace_strings):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)
            create_new_app(
                dummy_app=self.dummy_app,
                app_path=full_temp_path,
                model_name=self.model_name,
                app_label=self.app_label
            )

            expected_file_count = 23
            self.assertEqual(mock_replace_strings.call_count, expected_file_count)

    @mock.patch('allink_core.core.customisation.utils.rename')
    def test_create_new_app_all_renamed(self, mock_rename_file):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)
            create_new_app(
                dummy_app=self.dummy_app,
                app_path=full_temp_path,
                model_name=self.model_name,
                app_label=self.app_label
            )

            expected_file_count = 28
            self.assertEqual(mock_rename_file.call_count, expected_file_count)

    def test_create_new_app_no_dummy_app_names(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)

            create_new_app(
                dummy_app=self.dummy_app,
                app_path=full_temp_path,
                model_name=self.model_name,
                app_label=self.app_label
            )

            not_expected = ['dummy_app', 'dummyapp']
            all_dirs = list()
            all_files = list()
            for root, dirs, files in os.walk(full_temp_path):
                all_dirs.extend(dirs)
                all_files.extend(files)

            self.assertFalse([d for d in all_dirs if any(xs in d for xs in not_expected)])
            self.assertFalse([f for f in all_files if any(xs in f for xs in not_expected)])


class CustomisationForkAppTestCase(TestCase):
    dummy_app = 'allink_core.core.customisation.dummy_fork_app_minimum'
    app_label = 'news'

    expected_dirs = ['migrations', 'tests']
    expected_files = [
        'admin.py',
        'cms_apps.py',
        'cms_menus.py',
        'cms_plugins.py',
        'cms_toolbars.py',
        'config.py',
        'managers.py',
        'models.py',
    ]
    not_expected = ['dummy_app', 'dummyapp', 'DummyApp']

    def test_fork_allink_no_allink_app_with_name(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)

            with self.assertRaisesRegex(ValueError, 'There is no allink_core app'):
                fork_allink_app(
                    dummy_app=self.dummy_app,
                    app_path=full_temp_path,
                    app_label='wrong_app_label'
                )

    def test_fork_allink_app_no_dummy_app_names(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)

            fork_allink_app(
                dummy_app=self.dummy_app,
                app_path=full_temp_path,
                app_label=self.app_label
            )

            all_dirs = list()
            all_files = list()
            for root, dirs, files in os.walk(full_temp_path):
                all_dirs.extend(dirs)
                all_files.extend(files)

            self.assertFalse([d for d in all_dirs if any(xs in d for xs in self.not_expected)])
            self.assertFalse([f for f in all_files if any(xs in f for xs in self.not_expected)])

    def test_fork_allink_all_files(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)

            fork_allink_app(
                dummy_app=self.dummy_app,
                app_path=full_temp_path,
                app_label=self.app_label
            )

            all_dirs = list()
            all_files = list()
            for root, dirs, files in os.walk(full_temp_path):
                all_dirs.extend(dirs)
                all_files.extend(files)

            self.assertTrue([d for d in all_dirs if any(xs in d for xs in self.expected_dirs)])
            self.assertTrue([f for f in all_files if any(xs in f for xs in self.expected_files)])

    def test_rename_dummy_naming(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)

            fork_allink_app(
                dummy_app=self.dummy_app,
                app_path=full_temp_path,
                app_label=self.app_label
            )

            for root, dirs, files in os.walk(full_temp_path):
                # test strings which should not be in this file
                for file in files:
                    if file in self.expected_files:
                        with open(os.path.join(root, file), encoding='utf-8') as f:
                            s = f.read()
                            self.assertFalse(any(string in s for string in self.not_expected))
