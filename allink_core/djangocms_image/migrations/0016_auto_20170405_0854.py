# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0015_remove_allinkimageplugin_link_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='picture',
            field=filer.fields.image.FilerImageField(related_name='djangocms_image_allinkimageplugin_picture', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Image', to='filer.Image', null=True),
        ),
    ]
