# Generated by Django 2.1.8 on 2019-07-04 13:38

from django.db import migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ('-entry_date',), 'verbose_name': 'News entry', 'verbose_name_plural': 'News'},
        ),
        migrations.RemoveField(
            model_name='news',
            name='sort_order',
        ),
        migrations.AddField(
            model_name='news',
            name='entry_date',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='Entry Date'),
        ),
    ]
