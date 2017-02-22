# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import djangocms_text_ckeditor.fields
import parler.models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0006_auto_20160623_1627'),
        ('allink_categories', '0010_auto_20161209_0311'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkTerms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('end', models.DateTimeField(null=True, verbose_name='end', blank=True)),
                ('og_title', models.CharField(help_text='Title when shared on Facebook.', max_length=255, null=True, verbose_name='og:title', blank=True)),
                ('og_description', models.CharField(help_text='Description when shared on Facebook.', max_length=255, null=True, verbose_name='og:description', blank=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('status', models.IntegerField(default=10, verbose_name='Status', choices=[(10, 'Draft'), (20, 'Published'), (30, 'Archived')])),
                ('categories', models.ManyToManyField(to='allink_categories.AllinkCategory', blank=True)),
                ('og_image', filer.fields.image.FilerImageField(blank=True, to='filer.Image', help_text='Preview image when page/post is shared on Facebook. <br>Min. 1200 x 630 for best results.', null=True, verbose_name='og:Image')),
            ],
            options={
                'verbose_name': 'Terms of Service',
                'verbose_name_plural': 'Terms of Service',
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='AllinkTermsTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('text', djangocms_text_ckeditor.fields.HTMLField(verbose_name='Terms Text')),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='allink_terms.AllinkTerms', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'allink_terms_allinkterms_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'Terms of Service Translation',
            },
        ),
        migrations.AlterUniqueTogether(
            name='allinktermstranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
