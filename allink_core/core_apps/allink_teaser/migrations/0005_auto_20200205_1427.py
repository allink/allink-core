# Generated by Django 2.2.7 on 2020-02-05 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_teaser', '0004_allinkteaserplugin_softpage_enabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkteaserplugin',
            name='softpage_enabled',
            field=models.BooleanField(default=False, help_text='If checked, the detail view of an entry will be displayed in a "softpage". Otherwise the page will be reloaded.', verbose_name='Show detailed information in Softpage'),
        ),
    ]
