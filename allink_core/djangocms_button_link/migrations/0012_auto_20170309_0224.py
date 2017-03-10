# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import allink_core.allink_base.models.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0011_auto_20170221_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='extra_css_classes',
            field=allink_core.allink_base.models.model_fields.Classes(default=b'', help_text='Space separated classes that are added to the list of classes.', verbose_name='Css Classes', blank=True),
        ),
    ]
