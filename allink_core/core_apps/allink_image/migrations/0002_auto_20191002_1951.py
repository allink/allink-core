# Generated by Django 2.1.10 on 2019-10-02 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_image', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkimageplugin',
            name='link_target',
            field=models.IntegerField(blank=True, choices=[(1, 'New window'), (2, 'Softpage'), (4, 'Lightbox (Forms)'), (5, 'Lightbox (Image)'), (6, 'Lightbox (Default)')], null=True, verbose_name='Link Target'),
        ),
    ]
