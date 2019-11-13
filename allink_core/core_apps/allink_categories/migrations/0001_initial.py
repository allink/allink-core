# Generated by Django 2.1.8 on 2019-07-02 17:18

import aldryn_translation_tools.models
import allink_core.core.models.mixins
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lft', models.PositiveIntegerField(db_index=True)),
                ('rgt', models.PositiveIntegerField(db_index=True)),
                ('tree_id', models.PositiveIntegerField(db_index=True)),
                ('depth', models.PositiveIntegerField(db_index=True)),
                ('model_names', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, help_text='Please specify the app which uses this categories. All apps specified in parent category are automatically added.', null=True, size=None)),
                ('tag', models.CharField(blank=True, help_text='auto-generated categories use this tag, to identify which app generated the category.', max_length=80, null=True, verbose_name='Tag')),
                ('identifier', models.CharField(blank=True, help_text='Identifier used for backward reference on a app model. (e.g display category name on People app, e.g Marketing)', max_length=50, null=True, verbose_name='Identifier')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(allink_core.core.models.mixins.AllinkTranslatedAutoSlugifyMixin, aldryn_translation_tools.models.TranslationHelperMixin, parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='AllinkCategoryTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(default='', max_length=255, verbose_name='name')),
                ('slug', models.SlugField(blank=True, default='', help_text='Provide a “slug” or leave blank for an automatically generated one.', max_length=255, verbose_name='slug')),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='allink_categories.AllinkCategory')),
            ],
            options={
                'verbose_name': 'Category Translation',
                'db_table': 'allink_categories_allinkcategory_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
        ),
        migrations.AlterUniqueTogether(
            name='allinkcategorytranslation',
            unique_together={('language_code', 'master'), ('language_code', 'slug')},
        ),
    ]