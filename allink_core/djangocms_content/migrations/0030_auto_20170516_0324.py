# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0029_auto_20170511_0839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='title_size',
            field=models.CharField(max_length=50, default='h1', verbose_name='Section Title Size', choices=[('h1', 'Title Large'), ('h2', 'Title Medium'), ('h3', 'Title Small')]),
        ),
    ]
