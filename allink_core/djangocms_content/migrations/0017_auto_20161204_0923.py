# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0016_auto_20161204_0917'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allinkcontent',
            old_name='css_classes',
            new_name='extra_css_classes',
        ),
    ]
