# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0033_auto_20161222_0525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='template',
            field=models.CharField(default=(b'col-1', b'1 Column'), help_text='Choose a template.', max_length=50, verbose_name='Template', choices=[(b'col-1', b'1 Column'), (b'col-1-1', b'2 Columns (1:1)'), (b'col-2-1', b'2 Columns (2:1)'), (b'col-1-2', b'2 Columns (1:2)'), (b'col-3', b'3 Columns')]),
        ),
    ]
