# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0015_auto_20170315_0449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentcolumnplugin',
            name='alignment_horizontal_desktop',
            field=models.CharField(choices=[(b'left', 'Left'), (b'center', 'Center'), (b'right', 'Right')], max_length=50, blank=True, help_text='This option overrides the projects default alignment for desktop. (Usually "left")', null=True, verbose_name='Alignment horizontal desktop'),
        ),
        migrations.AlterField(
            model_name='allinkcontentcolumnplugin',
            name='alignment_horizontal_mobile',
            field=models.CharField(choices=[(b'left', 'Left'), (b'center', 'Center'), (b'right', 'Right')], max_length=50, blank=True, help_text='This option overrides the projects default alignment for mobile. (Usually "left")', null=True, verbose_name='Alignment horizontal mobile'),
        ),
    ]
