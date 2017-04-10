# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_button_link', '0023_remove_allinkbuttonlinkplugin_link_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='link_anchor',
            field=models.CharField(help_text='Appends the value only after the internal or external link.Do <em>not</em> include a preceding "#" symbol.', max_length=255, verbose_name='Anchor', blank=True),
        ),
    ]
