# Generated by Django 2.2.16 on 2020-11-30 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_auto_20201113_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Zip Code'),
        ),
    ]