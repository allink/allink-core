# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0010_auto_20170221_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkconfig',
            name='blog_verbose',
            field=models.CharField(default='Blog entry', max_length=255, verbose_name='Blog verbose name'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='blog_verbose_plural',
            field=models.CharField(default='Blog', max_length=255, verbose_name='Blog verbose name plural'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='events_verbose',
            field=models.CharField(default='Event', max_length=255, verbose_name='Events verbose name'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='events_verbose_plural',
            field=models.CharField(default='Events', max_length=255, verbose_name='Events verbose name plural'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='locations_verbose',
            field=models.CharField(default='Location', max_length=255, verbose_name='Locations verbose name'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='locations_verbose_plural',
            field=models.CharField(default='Locations', max_length=255, verbose_name='Locations verbose name plural'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='members_verbose',
            field=models.CharField(default='Member', max_length=255, verbose_name='Members verbose name'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='members_verbose_plural',
            field=models.CharField(default='Members', max_length=255, verbose_name='Members verbose name plural'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='news_verbose',
            field=models.CharField(default='News entry', max_length=255, verbose_name='News verbose name'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='news_verbose_plural',
            field=models.CharField(default='News', max_length=255, verbose_name='News verbose name plural'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='people_verbose',
            field=models.CharField(default='Person', max_length=255, verbose_name='People verbose name'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='people_verbose_plural',
            field=models.CharField(default='People', max_length=255, verbose_name='People verbose name plural'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='testimonials_verbose',
            field=models.CharField(default='Testimonial', max_length=255, verbose_name='Testimonials verbose name'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='testimonials_verbose_plural',
            field=models.CharField(default='Testimonials', max_length=255, verbose_name='Testimonials verbose name plural'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='work_verbose',
            field=models.CharField(default='Project/ Reference', max_length=255, verbose_name='Work verbose name'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='work_verbose_plural',
            field=models.CharField(default='Projects/ References', max_length=255, verbose_name='Work verbose name plural'),
        ),
    ]
