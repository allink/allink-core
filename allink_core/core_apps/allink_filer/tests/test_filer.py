import io
from django.test import TestCase
from django.test import TransactionTestCase
from django.core.files import File as DjangoFile
from filer.models import Folder

from allink_core.core_apps.allink_filer.utils import FilerStorage, TEST_IMAGE_PATH


class FilerStorageTestCase(TestCase):
    valid_folder_path = '/root_folder/folder1'
    valid_file_name = 'test.pdf'

    def setUp(self):
        self.filer_folder = Folder.objects.create(
            name='root__filer_folder'
        )
        self.file_folder_valid_path = '/root__filer_folder'
        self.filer_storage_valid = FilerStorage(
            folder_path=self.valid_folder_path,
            file_type='file',
            file_name=self.valid_file_name
        )
        self.file_object_bytes_io = io.BytesIO()

    def test_create_folder_static(self):
        created_folder = FilerStorage.create_folder(
            folder_path=self.valid_folder_path
        )
        self.assertEqual(created_folder.quoted_logical_path, self.valid_folder_path)

    def test_create_object_static(self):
        created_file = FilerStorage.create_object(folder=self.filer_folder, file=self.file_object_bytes_io, file_type='file', name=self.valid_file_name)

        self.assertEqual(created_file.original_filename, self.valid_file_name)
        self.assertEqual(created_file.logical_folder.quoted_logical_path, self.file_folder_valid_path)

    def test_create_object_static_path_variation(self):
        # with trailing slash

        created_file = FilerStorage.create_object(folder=self.filer_folder, file=self.file_object_bytes_io, file_type='file', name=self.valid_file_name)
        self.assertEqual(created_file.logical_folder.quoted_logical_path, self.file_folder_valid_path)

        # with leading slash

        created_file = FilerStorage.create_object(folder=self.filer_folder, file=self.file_object_bytes_io, file_type='file', name=self.valid_file_name)
        self.assertEqual(created_file.logical_folder.quoted_logical_path, self.file_folder_valid_path)

        # with leading and trailing slash

        created_file = FilerStorage.create_object(folder=self.filer_folder, file=self.file_object_bytes_io, file_type='file', name=self.valid_file_name)
        self.assertEqual(created_file.logical_folder.quoted_logical_path, self.file_folder_valid_path)

        # no file extension

        created_file = FilerStorage.create_object(folder=self.filer_folder, file=self.file_object_bytes_io, file_type='file', name='test_invalidpdf')

        self.assertEqual(created_file.original_filename, 'test_invalidpdf')
        self.assertEqual(created_file.logical_folder.quoted_logical_path, self.file_folder_valid_path)

    def test_save_bytes_io(self):
        created_folder, created_file = self.filer_storage_valid.save(file=self.file_object_bytes_io)
        self.assertEqual(created_file.original_filename, self.valid_file_name)
        self.assertEqual(created_file.logical_folder.quoted_logical_path, self.valid_folder_path)

        self.assertEqual(created_folder.quoted_logical_path, self.valid_folder_path)

    def test_save_string_io(self):
        file_object = io.StringIO()

        created_folder, created_file = self.filer_storage_valid.save(file=file_object)
        self.assertEqual(created_file.original_filename, self.valid_file_name)
        self.assertEqual(created_file.logical_folder.quoted_logical_path, self.valid_folder_path)

        self.assertEqual(created_folder.quoted_logical_path, self.valid_folder_path)

    def test_save_python_file_open(self):
        with open(self.valid_file_name, 'w+b') as self.file_object_bytes_io:
            created_folder, created_file = self.filer_storage_valid.save(file=self.file_object_bytes_io)
        self.assertEqual(created_file.original_filename, self.valid_file_name)
        self.assertEqual(created_file.logical_folder.quoted_logical_path, self.valid_folder_path)

        self.assertEqual(created_folder.quoted_logical_path, self.valid_folder_path)

    def test_save_django_file(self):
        django_file = DjangoFile(
            file=self.file_object_bytes_io,
            name=None
        )
        created_folder, created_file = self.filer_storage_valid.save(file=django_file)
        self.assertEqual(created_file.original_filename, self.valid_file_name)
        self.assertEqual(created_file.logical_folder.quoted_logical_path, self.valid_folder_path)

        self.assertEqual(created_folder.quoted_logical_path, self.valid_folder_path)

    def test_create_object_stimage(self):
        created_file = FilerStorage.create_object(folder=self.filer_folder, file=self.file_object_bytes_io, file_type='image', name=self.valid_file_name)

        self.assertEqual(created_file.original_filename, self.valid_file_name)
        self.assertEqual(created_file.logical_folder.quoted_logical_path, self.file_folder_valid_path)

    def test_create_object_static_path_variaimage(self):
        # with trailing slash

        created_file = FilerStorage.create_object(folder=self.filer_folder, file=self.file_object_bytes_io, file_type='image', name=self.valid_file_name)
        self.assertEqual(created_file.logical_folder.quoted_logical_path, self.file_folder_valid_path)

        # with leading slash

        created_file = FilerStorage.create_object(folder=self.filer_folder, file=self.file_object_bytes_io, file_type='image', name=self.valid_file_name)
        self.assertEqual(created_file.logical_folder.quoted_logical_path, self.file_folder_valid_path)

        # with leading and trailing slash

        created_file = FilerStorage.create_object(folder=self.filer_folder, file=self.file_object_bytes_io, file_type='image', name=self.valid_file_name)
        self.assertEqual(created_file.logical_folder.quoted_logical_path, self.file_folder_valid_path)

        # no file extension

        created_file = FilerStorage.create_object(folder=self.filer_folder, file=self.file_object_bytes_io, file_type='image', name='test_invalidpdf')

        self.assertEqual(created_file.original_filename, 'test_invalidpdf')
        self.assertEqual(created_file.logical_folder.quoted_logical_path, self.file_folder_valid_path)

    def test_delete_duplicates(self):
        FilerStorage.create_object(folder=self.filer_folder, file=self.file_object_bytes_io, file_type='image', name=self.valid_file_name)
        FilerStorage.create_object(folder=self.filer_folder, file=self.file_object_bytes_io, file_type='image', name=self.valid_file_name)
        from filer.models import Image
        self.assertEqual(Image.objects.all().count(), 1)
