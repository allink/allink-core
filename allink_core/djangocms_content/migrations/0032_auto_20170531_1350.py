# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0031_allinkcontentplugin_ignore_in_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='ignore_in_pdf',
            field=models.BooleanField(default=False, help_text='If checked, the content plugin will be ignored when generting a pdf.', verbose_name='Ignore for pdf export'),
        ),
    ]
