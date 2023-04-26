# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-07-04 17:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonialsappcontentplugin',
            name='load_more_button_text',
            field=models.CharField(blank=True, help_text='If left blank, a default text will be used. <br>Note: Should the default text be adjusted site-wide, please contact the project manager (such changes can be made on a code level)', max_length=255, null=True, verbose_name='Text for "Load .."-Button'),
        ),
        migrations.AlterField(
            model_name='testimonialsappcontentplugin',
            name='pagination_type',
            field=models.CharField(choices=[('no', 'None'), ('load', 'Add "Load more"-Button'), ('load_rest', 'Add "Load all"-Button')], default=('no', 'None'), max_length=50, verbose_name='Pagination Type'),
        ),
    ]