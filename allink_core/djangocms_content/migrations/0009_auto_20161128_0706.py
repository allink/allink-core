# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0008_auto_20161114_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='overlay_styles_enabled',
            field=models.BooleanField(default=True, help_text='If checked, the predefined overlay styles are applied (suitable when text is over an image/video)', verbose_name='Activate overlay styles'),
        ),
        migrations.AlterField(
            model_name='content',
            name='template',
            field=models.CharField(default=(b'col-1', b'1 Column'), help_text='Choose a template. This settings can NOT be changed after the content has been saved.', max_length=50, verbose_name='Template', choices=[(b'col-1', b'1 Column'), (b'col-1-1', b'2 Columns (1:1)'), (b'col-2-1', b'2 Columns (2:1)'), (b'col-1-2', b'2 Columns (1:2)'), (b'col-3', b'3 Columns')]),
        ),
    ]
