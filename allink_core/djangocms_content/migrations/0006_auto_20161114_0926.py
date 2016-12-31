# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0005_auto_20161114_0434'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='container_bg_image',
            new_name='bg_image_inner_container',
        ),
        migrations.RenameField(
            model_name='content',
            old_name='bg_image',
            new_name='bg_image_outer_container',
        ),
        migrations.RenameField(
            model_name='content',
            old_name='container',
            new_name='container_enabled',
        ),
        migrations.RemoveField(
            model_name='content',
            name='parallax',
        ),
        migrations.AddField(
            model_name='content',
            name='parallax_enabled',
            field=models.BooleanField(default=False, help_text='TBD: Disable until background image is set.', verbose_name='Activate Parallax effect'),
        ),
        migrations.AlterField(
            model_name='content',
            name='template',
            field=models.CharField(default=(b'col-1', b'1 Column'), help_text='Choose a ', max_length=50, verbose_name='Template', choices=[(b'col-1', b'1 Column'), (b'col-1-1', b'2 Columns (1:1)'), (b'col-2-1', b'2 Columns (2:1)'), (b'col-1-2', b'2 Columns (1:2)'), (b'col-3', b'3 Columns')]),
        ),
        migrations.AlterField(
            model_name='contentcolumn',
            name='template',
            field=models.CharField(default=b'col-1', max_length=50, verbose_name='Template', choices=[(b'col-1', b'1 Column'), (b'col-1-1', b'2 Columns (1:1)'), (b'col-2-1', b'2 Columns (2:1)'), (b'col-1-2', b'2 Columns (1:2)'), (b'col-3', b'3 Columns')]),
        ),
    ]
