# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0015_auto_20161201_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkcontent',
            name='bg_color_enabled',
        ),
        migrations.AddField(
            model_name='allinkcontent',
            name='bg_color',
            field=models.CharField(blank=True, max_length=7, null=True, verbose_name='Set a predefined background color', choices=[(b'primary', b'#000000'), (b'secondary', b'#373a3c'), (b'foo', b'#373a3c'), (b'foo', b'#373a3c'), (b'foo', b'#373a3c'), (b'foo', b'#373a3c')]),
        ),
    ]
