# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0023_auto_20170403_0409'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkcontentcolumnplugin',
            name='alignment_vertikal_desktop',
            field=models.CharField(choices=[(b'top', 'Top'), (b'middle', 'Middle'), (b'bottom', 'Bottom')], max_length=50, blank=True, help_text='This option overrides the projects default alignment for desktop. (Usually "top")', null=True, verbose_name='Alignment vertical desktop'),
        ),
    ]
