# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_instagram', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkinstagramplugin',
            name='account',
            field=models.CharField(help_text='Instagram account name', max_length=255, verbose_name='Compte'),
        ),
        migrations.AlterField(
            model_name='allinkinstagramplugin',
            name='template',
            field=models.CharField(default=(b'grid_static', b'Grid (Static)'), help_text='Choose a template.', max_length=50, verbose_name='Gabarit', choices=[(b'grid_static', b'Grid (Static)')]),
        ),
        migrations.AlterField(
            model_name='allinkinstagramplugin',
            name='title',
            field=models.CharField(help_text='The section title', max_length=255, null=True, verbose_name='Titre', blank=True),
        ),
    ]
