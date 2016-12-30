# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0004_contentcolumn_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='bg_image',
            field=filer.fields.image.FilerImageField(related_name='content_bg_image', blank=True, to='filer.Image', help_text='Dimensions TBD', null=True, verbose_name='Background-Image (Outer Container)'),
        ),
        migrations.AlterField(
            model_name='content',
            name='container',
            field=models.BooleanField(default=True, help_text='If checked, an inner container with a maximum width is added', verbose_name='Display columns within container'),
        ),
        migrations.AlterField(
            model_name='content',
            name='container_bg_image',
            field=filer.fields.image.FilerImageField(related_name='content_container_bg_image', blank=True, to='filer.Image', help_text='Dimensions TBD', null=True, verbose_name='Background-Image (Inner Container)'),
        ),
        migrations.AlterField(
            model_name='content',
            name='css_classes',
            field=models.CharField(help_text='Comma separated class names. Only letters, numbers, hyphen and underscores are allowed in class names.', max_length=255, null=True, verbose_name='CSS Classes', blank=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='parallax',
            field=models.BooleanField(default=False, help_text='Requires the ', verbose_name='Add Parallax effect'),
        ),
        migrations.AlterField(
            model_name='content',
            name='template',
            field=models.CharField(default=(b'col-1', b'1 Column'), help_text='Choose a ', max_length=50, verbose_name='Template', choices=[(b'col-1', b'1 Column'), (b'col-1-1', b'2 Columns (1:1)'), (b'col-2-1', b'2 Columns (2:1)'), (b'col-2-1', b'2 Columns (1:2)'), (b'col-3', b'3 Columns')]),
        ),
        migrations.AlterField(
            model_name='content',
            name='title',
            field=models.CharField(help_text='The section title', max_length=255, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AlterField(
            model_name='contentcolumn',
            name='template',
            field=models.CharField(default=b'col-1', max_length=50, verbose_name='Template', choices=[(b'col-1', b'1 Column'), (b'col-1-1', b'2 Columns (1:1)'), (b'col-2-1', b'2 Columns (2:1)'), (b'col-2-1', b'2 Columns (1:2)'), (b'col-3', b'3 Columns')]),
        ),
    ]
