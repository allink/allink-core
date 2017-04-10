# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0016_auto_20170405_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='link_anchor',
            field=models.CharField(help_text='Appends the value only after the internal or external link.Do <em>not</em> include a preceding "#" symbol.', max_length=255, verbose_name='Anchor', blank=True),
        ),
    ]
