import io
import factory
from django.core.files import File
from django.contrib.auth import get_user_model
from PIL import Image as PILimage

from filer.models import Image

__all__ = ['UserFactory', 'FilerImageFactory']


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'allink user nummer %d' % n)
    email = factory.Sequence(lambda n: 'example_%s@example.com' % n)
    first_name = factory.Sequence(lambda n: 'Fritzli %d' % n)
    last_name = factory.Sequence(lambda n: 'Bühler %d' % n)
    password = factory.PostGenerationMethodCall('set_password', 'itcrowd')
    is_active = True
    is_superuser = True
    is_staff = True

    class Meta:
        model = get_user_model()


class FilerImageFactory(factory.DjangoModelFactory):
    """
    Create a Filer Image for filer.fields.image.FilerImageField.
    """

    class Meta:
        model = Image

    owner = factory.SubFactory(UserFactory)
    original_filename = factory.Faker("file_name", category="image")

    @factory.lazy_attribute
    def file(self):
        """
        Fill file field with generated image on the fly by PIL.
        Generated image is just a blank image of 100x100 with plain blue color.
        Returns:
            django.core.files.File: File object.
        """
        # ImageField (both django's and factory_boy's) require PIL.
        thumb = PILimage.new("RGB", (100, 100), "blue")
        thumb_io = io.BytesIO()
        thumb.save(thumb_io, format="JPEG")

        return File(thumb_io, name=self.original_filename)
