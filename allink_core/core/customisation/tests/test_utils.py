import tempfile
import os
from django.test import TestCase
from unittest import mock
from ..utils import copy_dummy_dir, create_new_app, replace_strings, rename_dir_or_file


class CustomisationNewAppTestCase(TestCase):
    dummy_app_path = 'allink_core/core/customisation/dummy_app'
    app_label = 'new_app'
    model_name = 'NewApp'

    expected_file_count = 23

    def test_copy_dummy_dir_already_exists(self):
        apps_dir = 'apps'
        with self.assertRaisesRegex(OSError, "'{}' directory already exists!".format(apps_dir)):
            copy_dummy_dir(dummy_app_path=self.dummy_app_path, app_path=apps_dir)

    def test_copy_dummy_dir_all_files_copied(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)
            copy_dummy_dir(dummy_app_path=self.dummy_app_path, app_path=full_temp_path)
            total_file_count = sum([len(files) for r, d, files in os.walk(full_temp_path)])
            expected_file_count = self.expected_file_count + 1  # including README.md
            self.assertEqual(total_file_count, expected_file_count)

    def test_rename_dummy_classes_in_one_file(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)
            copy_dummy_dir(dummy_app_path=self.dummy_app_path, app_path=full_temp_path)

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
            copy_dummy_dir(dummy_app_path=self.dummy_app_path, app_path=full_temp_path)

            replace = {
                'dummy_app': self.app_label,
                'dummyapp': self.model_name.lower(),
            }
            # file
            new_file = os.path.join(full_temp_path, 'templates', 'dummy_app', 'dummyapp_detail.html')
            rename_dir_or_file(path=new_file, replace=replace)
            renamed_file = os.path.join(full_temp_path, 'templates', 'dummy_app', 'newapp_detail.html')
            self.assertTrue(os.path.isfile(renamed_file))

            # dir
            new_dir = os.path.join(full_temp_path, 'templates', 'dummy_app')
            rename_dir_or_file(path=new_dir, replace=replace)
            renamed_dir = os.path.join(full_temp_path, 'templates', 'new_app')
            self.assertTrue(os.path.isdir(renamed_dir))

    @mock.patch('allink_core.core.customisation.utils.replace_strings')
    def test_create_new_app_all_files_string_replaced(self, mock_replace_strings):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)
            create_new_app(
                dummy_app_path=self.dummy_app_path,
                app_path=full_temp_path,
                app_label=self.app_label,
                model_name=self.model_name
            )

            total_file_count = sum([len(files) for r, d, files in os.walk(full_temp_path)])
            self.assertEqual(mock_replace_strings.call_count, total_file_count)

    @mock.patch('allink_core.core.customisation.utils.rename_dir_or_file')
    def test_create_new_app_all_renamed(self, mock_rename_file):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)
            create_new_app(
                dummy_app_path=self.dummy_app_path,
                app_path=full_temp_path,
                app_label=self.app_label,
                model_name=self.model_name
            )

            total_file_and_dir_count = sum([len(files) for r, d, files in os.walk(full_temp_path)]) \
                               + sum([len(dirs) for r, dirs, f in os.walk(full_temp_path)]) - 1
            self.assertEqual(mock_rename_file.call_count, total_file_and_dir_count)

    def test_create_new_app_no_dummy_app_names(self):
        with tempfile.TemporaryDirectory(prefix='temp_apps') as temp_apps_dir:
            full_temp_path = os.path.join(temp_apps_dir, self.app_label)

            create_new_app(
                dummy_app_path=self.dummy_app_path,
                app_path=full_temp_path,
                app_label=self.app_label,
                model_name=self.model_name
            )

            not_expected = ['dummy_app', 'dummyapp']
            all_dirs = list()
            all_files = list()
            for root, dirs, files in os.walk(full_temp_path):
                all_dirs.extend(dirs)
                all_files.extend(files)

            self.assertFalse([d for d in all_dirs if any(xs in d for xs in not_expected)])
            self.assertFalse([f for f in all_files if any(xs in f for xs in not_expected)])