# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0004_auto_20170119_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='template',
            field=models.CharField(default=(b'col-1', b'1 Column'), help_text='Choose a template.', max_length=50, verbose_name='Template', choices=[(b'col-1', b'1 Column'), (b'col-1-1', b'2 Columns (1:1)'), (b'col-2-1', b'2 Columns (2:1)'), (b'col-1-2', b'2 Columns (1:2)'), (b'col-3', b'3 Columns'), (b'col-4', b'4 Columns'), (b'col-5', b'5 Columns'), (b'col-6', b'6 Columns')]),
        ),
    ]
