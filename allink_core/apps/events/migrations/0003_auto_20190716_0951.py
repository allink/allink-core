# Generated by Django 2.1.10 on 2019-07-16 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20190704_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventstranslation',
            name='teaser_description',
            field=models.TextField(blank=True, default='', help_text='Page: no fallback.<br>App: fallback is field "lead".Please only use 80 to 120 characters. Best results will be achieved with around 100 characters.', verbose_name='Teaser description'),
        ),
    ]