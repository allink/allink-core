# Generated by Django 2.1.10 on 2019-10-02 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20190716_0951'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventsappcontentplugin',
            name='filter_fields',
        ),
    ]
