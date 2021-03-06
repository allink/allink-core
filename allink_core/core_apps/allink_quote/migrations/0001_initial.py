# Generated by Django 2.2.6 on 2019-11-14 18:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('cms', '0022_auto_20180620_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkQuotePlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='allink_quote_allinkquoteplugin', serialize=False, to='cms.CMSPlugin')),
                ('text', models.TextField(verbose_name='Quote Text')),
                ('author', models.CharField(blank=True, max_length=255, null=True, verbose_name='Author Name')),
                ('author_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Author Description')),
                ('author_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.FILER_IMAGE_MODEL, verbose_name='Author Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
