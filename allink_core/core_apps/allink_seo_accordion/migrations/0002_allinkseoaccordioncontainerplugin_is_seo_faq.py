# Generated by Django 2.2.13 on 2020-09-07 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_seo_accordion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allinkseoaccordioncontainerplugin',
            name='is_seo_faq',
            field=models.BooleanField(default=False, help_text='Enable to display accordion contents as questions/answers in search engine result pages', verbose_name='Enable SEO FAQ schema'),
        ),
    ]
