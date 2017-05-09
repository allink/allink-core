# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0018_auto_20170403_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkcategory',
            name='identifier',
            field=models.CharField(null=True, verbose_name='Identifier', blank=True, help_text='Identifier used for backward reference on a app model. (e.g display category name on People app, e.g Marketing)', max_length=50),
        ),
    ]
