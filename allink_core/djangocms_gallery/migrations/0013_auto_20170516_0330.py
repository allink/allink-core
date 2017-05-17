# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gallery', '0012_auto_20170516_0324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkgalleryplugin',
            name='title',
        ),
        migrations.RemoveField(
            model_name='allinkgalleryplugin',
            name='title_size',
        ),
    ]
