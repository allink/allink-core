# Generated by Django 2.2.13 on 2020-11-02 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0007_locationstranslation_teaser_link_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationstranslation',
            name='teaser_link_url',
            field=models.URLField(blank=True, help_text='Provide a valid URL to an external website.', max_length=500, null=True, verbose_name='External link'),
        ),
    ]
