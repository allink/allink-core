# Generated by Django 2.2.16 on 2021-02-10 13:26

from django.db import migrations
import django.db.models.deletion
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0012_file_mime_type'),
        ('allink_categories', '0002_auto_20191002_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkcategory',
            name='logo',
            field=filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='allink_categories_allinkcategory_logo', to='filer.File', verbose_name='Logo'),
        ),
    ]