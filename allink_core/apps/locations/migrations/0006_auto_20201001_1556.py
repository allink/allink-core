# Generated by Django 2.2.13 on 2020-10-01 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_auto_20191002_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationsappcontentplugin',
            name='load_more_link',
            field=models.URLField(blank=True, help_text='Link for Button Below Items if custom URL is chosen', null=True, verbose_name='Custom Load More Link'),
        ),
        migrations.AlterField(
            model_name='locationsappcontentplugin',
            name='pagination_type',
            field=models.CharField(choices=[('no', 'None'), ('load', 'Add "Load more"-Button'), ('load_rest', 'Add "Load all"-Button'), ('load_url', 'Add "Custom URL"-Button')], default=('no', 'None'), max_length=50, verbose_name='Pagination Type'),
        ),
    ]
