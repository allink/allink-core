# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0018_auto_20161204_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontent',
            name='bg_color',
            field=models.IntegerField(blank=True, null=True, verbose_name='Set a predefined background color', choices=[(0, b'#000000'), (1, b'#373a3c'), (2, b'#373a3c')]),
        ),
    ]
