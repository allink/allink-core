from cms.models import CMSPlugin
from django.db import models
from djangocms_text_ckeditor.fields import HTMLField


class AllinkListMulticolPlugin(CMSPlugin):
    COLUMN_CHOICES = [
        (0, 'Two Columns'),
        (1, 'Three Columns'),
    ]

    text = HTMLField(
        'Text',
        help_text='Numbered and bulleted lists in this text will automatically be displayed in multiple columns.',
        blank=True,
        null=True,
    )

    column_mode = models.IntegerField(
        verbose_name='Columns',
        choices=COLUMN_CHOICES,
        default=0,
    )
