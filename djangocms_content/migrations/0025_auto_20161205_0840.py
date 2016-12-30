# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0024_auto_20161205_0826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='video_mobile_image_alignment',
            field=models.CharField(default=b'center', help_text='TBD Define which part of the image must be visible. Because we use the available space, there is a chance that a part (left and/or right) is not visible.', max_length=50, verbose_name='Mobile Image Alignment (horizontal)', choices=[(b'left', 'Left'), (b'center', 'Center'), (b'right', 'Right')]),
        ),
    ]
