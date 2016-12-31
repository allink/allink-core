# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0003_auto_20161111_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentcolumn',
            name='template',
            field=models.CharField(default=b'1_col', max_length=50, verbose_name='Template', choices=[(b'1_col', b'1 \xe2\x80\x93 col')]),
        ),
    ]
