# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0014_auto_20170315_0346'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkcontentcolumnplugin',
            name='alignment_horizontal_desktop',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Alignment horizontal desktop', choices=[(b'left', 'Left'), (b'center', 'Center'), (b'right', 'Right')]),
        ),
        migrations.AddField(
            model_name='allinkcontentcolumnplugin',
            name='alignment_horizontal_mobile',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Alignment horizontal mobile', choices=[(b'left', 'Left'), (b'center', 'Center'), (b'right', 'Right')]),
        ),
    ]
