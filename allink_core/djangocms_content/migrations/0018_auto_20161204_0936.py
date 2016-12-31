# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0017_auto_20161204_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontent',
            name='bg_color',
            field=models.IntegerField(blank=True, null=True, verbose_name='Set a predefined background color', choices=[(1, b'#000000'), (2, b'#373a3c'), (3, b'#373a3c'), (4, b'#373a3c'), (5, b'#373a3c'), (6, b'#373a3c')]),
        ),
    ]
