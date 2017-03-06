# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0011_auto_20170301_0320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='allinkconfig',
            old_name='testimonials_verbose',
            new_name='testimonial_verbose',
        ),
        migrations.RenameField(
            model_name='allinkconfig',
            old_name='testimonials_verbose_plural',
            new_name='testimonial_verbose_plural',
        ),
    ]
