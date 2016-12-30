# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('filer', '0006_auto_20160623_1627'),
        ('djangocms_content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_content_content', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title', blank=True)),
                ('template', models.CharField(default=b'1_col', max_length=50, verbose_name='Template', choices=[(b'1_col', '1 \u2013 col')])),
                ('container', models.BooleanField(default=True, verbose_name='Display container')),
                ('parallax', models.BooleanField(default=False, verbose_name='Parallax')),
                ('css_classes', models.CharField(help_text='Seperate the all the CSS classes with ",".', max_length=255, null=True, verbose_name='CSS Classes', blank=True)),
                ('bg_image', filer.fields.image.FilerImageField(related_name='content_bg_image', blank=True, to='filer.Image', help_text='Width: 1300px', null=True, verbose_name='Background-Image')),
                ('container_bg_image', filer.fields.image.FilerImageField(related_name='content_container_bg_image', blank=True, to='filer.Image', help_text='Width: 1300px', null=True, verbose_name='Background-Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.RemoveField(
            model_name='multicolumn',
            name='bg_image',
        ),
        migrations.RemoveField(
            model_name='multicolumn',
            name='cmsplugin_ptr',
        ),
        migrations.DeleteModel(
            name='Multicolumn',
        ),
    ]
