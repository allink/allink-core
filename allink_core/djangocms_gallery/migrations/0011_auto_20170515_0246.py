# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gallery', '0010_auto_20170407_0814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkgalleryplugin',
            name='template',
            field=models.CharField(help_text='Choose a template.', max_length=50, default=('slider', 'Slider'), verbose_name='Template'),
        ),
    ]
