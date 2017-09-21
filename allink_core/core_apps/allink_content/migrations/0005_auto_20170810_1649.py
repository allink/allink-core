# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-08-10 16:49
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('allink_content', '0004_auto_20170725_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='bg_image_outer_container',
            field=filer.fields.image.FilerImageField(blank=True, help_text='Optional: Set a background image for the content section.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='allink_content_allinkcontentplugin_bg_image', to='filer.Image', verbose_name='Background-Image'),
        ),
    ]