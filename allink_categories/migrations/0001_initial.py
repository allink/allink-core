# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import parler.models
import aldryn_translation_tools.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lft', models.PositiveIntegerField(db_index=True)),
                ('rgt', models.PositiveIntegerField(db_index=True)),
                ('tree_id', models.PositiveIntegerField(db_index=True)),
                ('depth', models.PositiveIntegerField(db_index=True)),
                ('app_category_label', models.CharField(help_text='Please specify the app which uses this categories.', max_length=50, verbose_name='Project app')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(aldryn_translation_tools.models.TranslatedAutoSlugifyMixin, aldryn_translation_tools.models.TranslationHelperMixin, parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='AllinkCategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('name', models.CharField(default='', max_length=255, verbose_name='name')),
                ('slug', models.SlugField(default='', max_length=255, blank=True, help_text='Provide a \u201cslug\u201d or leave blank for an automatically generated one.', verbose_name='slug')),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='allink_categories.AllinkCategory', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'allink_categories_allinkcategory_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'category Translation',
            },
        ),
        migrations.AlterUniqueTogether(
            name='allinkcategorytranslation',
            unique_together=set([('language_code', 'master'), ('language_code', 'slug')]),
        ),
    ]
