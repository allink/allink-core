# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0030_auto_20161213_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkcontentplugin',
            name='full_height_enabled',
            field=models.BooleanField(default=False, help_text="If checked, the section will use the available height of the device's/browser's screen.", verbose_name='Activate "full height" mode'),
        ),
        migrations.AddField(
            model_name='allinkcontentplugin',
            name='title_size',
            field=models.CharField(default=b'h1', max_length=50, verbose_name='Section Title Size', choices=[(b'h1', 'Title Large'), (b'h2', 'Title Medium')]),
        ),
    ]
