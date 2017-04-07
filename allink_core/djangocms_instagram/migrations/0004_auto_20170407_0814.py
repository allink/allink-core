# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_instagram', '0003_auto_20170322_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkinstagramplugin',
            name='ordering',
            field=models.CharField(default=('default', '---------'), max_length=50, choices=[('default', '---------'), ('latest', 'latest first'), ('random', 'random')], verbose_name='Sort order', help_text='Choose a order.'),
        ),
        migrations.AlterField(
            model_name='allinkinstagramplugin',
            name='template',
            field=models.CharField(default=('grid_static', 'Grid (Static)'), max_length=50, choices=[('grid_static', 'Grid (Static)')], verbose_name='Template', help_text='Choose a template.'),
        ),
    ]
