# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0014_allinkimageplugin_project_css_classes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkimageplugin',
            name='link_page',
        ),
    ]
