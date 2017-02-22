# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0008_auto_20170112_0632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkconfig',
            name='default_recipient',
        ),
        migrations.RemoveField(
            model_name='allinkconfig',
            name='default_sender',
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='default_base_title',
            field=models.CharField(help_text='Default base title, Is also used for default base og:title when page/post is shared on Facebook. <br>. If not supplied the name form Django Sites will be used instead.', max_length=50, null=True, verbose_name='base title', blank=True),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='mask_icon_color',
            field=models.CharField(default=b'#282828', help_text='Mask icon color for safari-pinned-tab.svg', max_length=7, verbose_name='Mask icon color'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='msapplication_tilecolor',
            field=models.CharField(default=b'#282828', help_text='MS application TitleColor Field', max_length=7, verbose_name='msapplication TileColor'),
        ),
        migrations.AddField(
            model_name='allinkconfig',
            name='theme_color',
            field=models.CharField(default=b'#ffffff', help_text='Theme color for Android Chrome', max_length=7, verbose_name='Theme Color'),
        ),
        migrations.AlterField(
            model_name='allinkconfig',
            name='default_og_image',
            field=filer.fields.image.FilerImageField(blank=True, to='filer.Image', help_text='Default preview image when page/post is shared on Facebook. <br>Min. 1200 x 630 for best results.', null=True, verbose_name='og:image'),
        ),
    ]
