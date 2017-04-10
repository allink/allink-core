# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0025_auto_20170404_0635'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkcontentplugin',
            name='anchor',
            field=models.CharField(help_text='Sets the id of the div section. (Use site-wide unique id.)Do <em>not</em> include a preceding "#" symbol.', max_length=255, verbose_name='Anchor', blank=True),
        ),
    ]
