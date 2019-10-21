# Generated by Django 2.1.10 on 2019-10-02 20:20

import allink_core.core.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_remove_locationsappcontentplugin_filter_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationsappcontentplugin',
            name='manual_entries',
            field=allink_core.core.models.fields.SortedM2MModelField(blank=True, help_text='Select and arrange specific entries, or, leave blank to select all. (If manual entries are selected the category filtering will be applied as well.)', to='locations.Locations'),
        ),
    ]
