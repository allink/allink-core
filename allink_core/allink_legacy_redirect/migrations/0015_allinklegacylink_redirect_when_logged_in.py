# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_legacy_redirect', '0014_auto_20170519_0136'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinklegacylink',
            name='redirect_when_logged_in',
            field=models.BooleanField(verbose_name='Redirect when logged in', help_text='If True, current site will be redirected to translated language. If False, it redirects to the homepage', default=False),
        ),
    ]
