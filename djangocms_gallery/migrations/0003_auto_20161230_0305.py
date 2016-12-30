# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gallery', '0002_auto_20161223_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkgalleryplugin',
            name='template',
            field=models.CharField(default=(b'slider', b'Slider'), help_text='Choose a template.', max_length=50, verbose_name='Template', choices=[(b'slider', b'Slider'), (b'grid', b'Grid')]),
        ),
    ]
