# Generated by Django 2.2.12 on 2020-04-17 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allink_teaser', '0008_auto_20200417_1052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkteaserplugin',
            name='softpage_enabled',
        ),
    ]
