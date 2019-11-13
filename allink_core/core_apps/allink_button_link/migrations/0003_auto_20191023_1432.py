# Generated by Django 2.2.6 on 2019-10-23 14:32

import allink_core.core_apps.allink_button_link.model_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allink_button_link', '0002_auto_20191002_1951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='btn_context',
            field=allink_core.core_apps.allink_button_link.model_fields.Context(choices=[('default', 'Default'), ('primary', 'Primary')], default='default', max_length=255, verbose_name='Variation'),
        ),
        migrations.AlterField(
            model_name='allinkbuttonlinkplugin',
            name='txt_context',
            field=allink_core.core_apps.allink_button_link.model_fields.Context(blank=True, choices=[('', 'Default'), ('primary', 'Primary'), ('muted ', 'Muted')], default='', max_length=255, verbose_name='Context'),
        ),
    ]