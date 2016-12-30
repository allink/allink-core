# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0028_auto_20161207_0327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(parent_link=True, related_name='djangocms_content_allinkcontentplugin', primary_key=True, serialize=False, to='cms.CMSPlugin'),
        ),
    ]
