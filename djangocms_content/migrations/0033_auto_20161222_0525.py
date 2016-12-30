# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0032_auto_20161215_0455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentcolumnplugin',
            name='template',
            field=models.CharField(default=b'grid_dynamic', max_length=50, verbose_name='Template', choices=[(b'grid_dynamic', b'Grid (Dynamic)'), (b'grid_static', b'Grid (Static)'), (b'list', b'List'), (b'slider', b'Slider')]),
        ),
    ]
