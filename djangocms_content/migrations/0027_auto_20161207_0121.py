# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0026_auto_20161206_0700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentcolumnplugin',
            name='template',
            field=models.CharField(default=b'grid', max_length=50, verbose_name='Template', choices=[(b'grid', b'Grid'), (b'list', b'List')]),
        ),
    ]
