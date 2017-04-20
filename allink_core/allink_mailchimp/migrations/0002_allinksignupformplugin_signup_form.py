# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_mailchimp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinksignupformplugin',
            name='signup_form',
            field=models.CharField(verbose_name='Template', choices=[('simple', 'Simple'), ('advanced', 'Advanced')], default=('simple', 'Simple'), max_length=50, help_text='Choose a form.'),
        ),
    ]
