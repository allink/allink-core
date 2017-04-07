# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_gallery', '0009_auto_20170404_0632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkgalleryplugin',
            name='ratio',
            field=models.CharField(max_length=50, null=True, verbose_name='Ratio', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkgalleryplugin',
            name='template',
            field=models.CharField(default=('slider', 'Slider'), max_length=50, choices=[('slider', 'Slider')], verbose_name='Template', help_text='Choose a template.'),
        ),
        migrations.AlterField(
            model_name='allinkgalleryplugin',
            name='title_size',
            field=models.CharField(default='h1', max_length=50, choices=[('h1', 'Title Large'), ('h2', 'Title Medium')], verbose_name='Section Title Size'),
        ),
    ]
