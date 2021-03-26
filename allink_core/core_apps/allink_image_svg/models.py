from cms.models import CMSPlugin
from django.db import models

from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
import re

from filer.fields.file import FilerFileField

from allink_core.core.models import AllinkLinkFieldsModel


class AllinkImageSVGPlugin(AllinkLinkFieldsModel, CMSPlugin):
    picture = FilerFileField(
        verbose_name='Image',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_image',
    )

    is_inline = models.BooleanField(
        'Is inline',
        default=False,
        help_text="Check if the SVG will be inlined.",
    )

    is_fullwidth = models.BooleanField(
        'Is Fullwidth',
        default=True,
        help_text="Stretches the SVG to 100% width.",
    )

    def render_svg(self, **kwargs):
        """
        reads svg image and extracts <svg> tag.
        if not found or can not be read en empty string will be returned
        """
        if not self.picture:
            return ''

        pattern = r'<svg(.*)svg>'
        try:
            file_string = self.picture.file.read().decode("utf-8")
            if file_string:
                return mark_safe(re.search(pattern, file_string, flags=re.DOTALL)[0])
            else:
                return ''
        except OSError:
            return ''

    def clean(self):
        if self.picture and self.picture.extension not in ['svg']:
            raise ValidationError(
                'Incorrect file type: %(value)s',
                params={'value': self.picture.extension},
            )
