# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gallery', '0014_auto_20170516_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkgalleryplugin',
            name='auto_start_enabled',
            field=models.BooleanField(verbose_name='Autostart', default=True, help_text='This option enables autoplay for this gallery.'),
        ),
    ]
