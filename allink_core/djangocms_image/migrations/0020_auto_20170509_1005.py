# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0019_auto_20170509_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='bg_enabled',
            field=models.BooleanField(default=True, help_text='Show default image placeholder background color.<br><strong>Important:</strong> Disabling this option results in a transparent background even if a specific color is set (this makes sense when a transparent PNG image is used)', verbose_name='Placeholder Background Color'),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='icon_enabled',
            field=models.BooleanField(default=True, help_text='Show the icon that is used as long as the image is loading.<br><strong>Important:</strong> Disable this option if a transparent PNG image is used.', verbose_name='Loader Icon'),
        ),
    ]
