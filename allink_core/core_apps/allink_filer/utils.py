# -*- coding: utf-8 -*-
from django.core.files import File as DjangoFile
from filer.models import File, Image
from filer.models import Folder
from pathlib import Path
_base_url = None

TEST_IMAGE_PATH = 'allink_core/core_apps/allink_filer/tests/data/test_image.jpg'


class FilerStorage:
    """
    usage:
    new_file = FilerFileStorage(folder_path='root_folder/folder'), file_name='pdf.pdf')
    new_file.save(file=SomePythonFile)

    """

    FILE_TYPE_MAPPER = {
        'file':  File,
        'image': Image
    }

    def __init__(self, folder_path, file_type, file_name=None):
        self._folder_path = folder_path
        self._file_name = file_name
        self._file_type_mapper_key = file_type
        self._file_type = self.FILE_TYPE_MAPPER.get(file_type)

    @property
    def folder_path(self):
        """
        strips "/" from folder_path in case of invalid input
        :return:
        pathlib Path object
        """
        return Path(self._folder_path.strip("/"))

    @property
    def file_name(self):
        return self._file_name

    @property
    def file_type(self):
        return self._file_type

    @staticmethod
    def create_folder(folder_path):
        """
        creates or gets all the folders folder
        strips "/" from folder_path in case of invalid input
        :param folder_path:
        all folders in the path will be created
        :return:
        the deepest folder object which was created
        """
        parent = None
        parts = folder_path.parts if isinstance(folder_path, Path) else Path(folder_path.strip("/")).parts

        for name in parts:
            if parent:
                parent, _ = Folder.objects.get_or_create(name=name, parent=parent)
            else:
                parent, _ = Folder.objects.get_or_create(name=name)
        return parent

    @classmethod
    def create_object(cls, folder, file, file_type, name=None):
        """
        :param folder:
        the filer folder to save the file at
        :param file:
        the file object to save (e.g io.BytesIO() or python file)
        :param file_type:
        file_type in cls.FILE_TYPE_MAPPER
        :param name:
        the file name to save the file as
        :return:
        the saved filer file
        """
        if name is None:
            name = getattr(file, 'name', None)

        filer_class = cls.FILE_TYPE_MAPPER.get(file_type)

        new_object = filer_class(folder=folder, file=DjangoFile(file=file, name=name), original_filename=name)
        # delete duplicates
        filer_class.objects.filter(folder=folder, original_filename=name, sha1=new_object.sha1).delete()

        new_object.save()
        return new_object

    def save(self, file):
        """
        :param file:
        some file (e.g ByteIo())
        :return:
        the created folders and filer object
        """
        created_folder = FilerStorage.create_folder(self.folder_path)

        created_file = FilerStorage.create_object(
            folder=created_folder,
            name=self.file_name,
            file_type=self._file_type_mapper_key,
            file=file
        )

        return created_folder, created_file
