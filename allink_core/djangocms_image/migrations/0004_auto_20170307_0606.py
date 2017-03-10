# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0003_auto_20170302_0455'),
    ]

    operations = [
        migrations.RunSQL('''
            delete from djangocms_picture_picture;
            '''.format(app_label='djangocms_picture'))
    ]
