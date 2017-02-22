# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0009_auto_20170221_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkconfig',
            name='default_base_title',
            field=models.CharField(help_text='Default base title, Is also used for default base og:title when page/post is shared on Facebook. <br>If not supplied the name form Django Sites will be used instead.', max_length=50, null=True, verbose_name='Base title', blank=True),
        ),
    ]
