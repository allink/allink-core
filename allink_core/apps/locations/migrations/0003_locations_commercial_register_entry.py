# Generated by Django 2.1.10 on 2019-09-03 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20190716_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='commercial_register_entry',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Commercial register entry'),
        ),
    ]
