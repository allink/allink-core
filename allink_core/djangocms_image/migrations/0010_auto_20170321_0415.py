# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.file
import djangocms_attributes_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0009_auto_20170315_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='attributes',
            field=djangocms_attributes_field.fields.AttributesField(default=dict, verbose_name='Attributs', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='caption_text',
            field=models.TextField(help_text='Angaben wie Beschreibung, Zuschreibung, Copyright oder andere Informationen.', verbose_name='Legendentext', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='external_picture',
            field=models.URLField(help_text='\xdcberschreibt das vorhandene Bild, falls gegeben. Manche Optionen wie Zuschneiden sind f\xfcr externe Bilder nicht verf\xfcgbar.', max_length=255, verbose_name='Externes Bild', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='link_attributes',
            field=djangocms_attributes_field.fields.AttributesField(default=dict, verbose_name='Attributs', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='link_file',
            field=filer.fields.file.FilerFileField(verbose_name='fichier', blank=True, to='filer.File', null=True),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='link_mailto',
            field=models.EmailField(max_length=255, null=True, verbose_name='Adresse \xe9lectronique', blank=True),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='template',
            field=models.CharField(default=(b'default', b'Default'), help_text='Choose a template.', max_length=50, verbose_name='Gabarit', choices=[(b'default', b'Default')]),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='use_no_cropping',
            field=models.BooleanField(default=False, help_text='Gibt das RAW-Bild aus, ohne dieses zuzuschneiden.', verbose_name='Originalgr\xf6sse verwenden'),
        ),
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='width',
            field=models.PositiveIntegerField(help_text='Die Bildbreite als Zahl in Pixel. Beispiel: "720" und nicht "720px"', null=True, verbose_name='Breite', blank=True),
        ),
    ]
