# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gallery', '0013_auto_20170516_0330'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkgalleryplugin',
            name='counter_enabled',
            field=models.BooleanField(help_text='This option enables a gallery counter.', default=False, verbose_name='Gallery counter visible'),
        ),
        migrations.AddField(
            model_name='allinkgalleryplugin',
            name='fullscreen_enabled',
            field=models.BooleanField(help_text='This option enables a fullscreen button for this gallery.', default=False, verbose_name='Fullscreen option visible'),
        ),
    ]
