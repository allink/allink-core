# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0030_auto_20170516_0324'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkcontentplugin',
            name='ignore_in_pdf',
            field=models.BooleanField(verbose_name='Ignore for pdf export', default=False, help_text='If checked, the content plugin will not be ignored when generting a pdf.'),
        ),
    ]
