# Generated by Django 2.1.11 on 2019-10-17 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_video', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkvideofileplugin',
            name='auto_start_mobile_enabled',
            field=models.BooleanField(default=False, help_text='Caution: Autoplaying videos on mobile is not recommended. Use wisely.', verbose_name='Autostart mobile'),
        ),
    ]
