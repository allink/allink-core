# Generated by Django 2.2.9 on 2020-03-24 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allink_content', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allinkcontentplugin',
            name='project_on_screen_effect',
        ),
    ]
