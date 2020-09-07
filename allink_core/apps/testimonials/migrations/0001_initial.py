# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-06-21 17:35
from __future__ import unicode_literals

import aldryn_common.admin_fields.sortedm2m
import aldryn_translation_tools.models
import allink_core.core.models.mixins
import cms.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djangocms_text_ckeditor.fields
import filer.fields.image
import model_utils.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0007_auto_20161016_1055'),
        ('allink_categories', '0001_initial'),
        ('cms', '0016_auto_20160608_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('disable_base_title', models.BooleanField(default=False, help_text='If disabled, only the page title will be shown. Everything behind and including the "|" will be removed.', verbose_name='Disable base title')),
                ('first_name', models.CharField(default='', max_length=255, verbose_name='First Name')),
                ('last_name', models.CharField(default='', max_length=255, verbose_name='Last Name')),
                ('sort_order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
                ('auto_generated_category', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auto_generated_from_testimonials', to='allink_categories.AllinkCategory')),
                ('categories', models.ManyToManyField(blank=True, to='allink_categories.AllinkCategory')),
                ('content_placeholder', cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='testimonials_testimonials_content_placeholder', slotname='testimonials_content', to='cms.Placeholder')),
                ('header_placeholder', cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='testimonials_testimonials_header_placeholder', slotname='testimonials_header', to='cms.Placeholder')),
                ('og_image', filer.fields.image.FilerImageField(blank=True, help_text='Preview image when page/post is shared on Facebook/ Twitter. <br>Min. 1200 x 630 for best results. If not set, the one from the preview image will be used, if not set or not in a app context, the one defined in allink_settings will be used.', null=True, on_delete=django.db.models.deletion.CASCADE, to='filer.Image', verbose_name='og:Image')),
                ('preview_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='testimonials_testimonials_preview_image', to='filer.Image', verbose_name='Preview Image')),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
                'abstract': False,
                'ordering': ('sort_order',),
            },
            bases=(aldryn_translation_tools.models.TranslationHelperMixin, allink_core.core.models.mixins.AllinkTranslatedAutoSlugifyMixin, parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TestimonialsAppContentPlugin',
            fields=[
                ('manual_ordering', models.CharField(blank=True, max_length=50, null=True)),
                ('filter_fields', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, default=None, null=True, size=None)),
                ('template', models.CharField(help_text='Choose a template.', max_length=50, verbose_name='Template')),
                ('category_navigation_enabled', models.BooleanField(default=False, help_text='If checked, a filter navigation with all selected categories is displayed.<br>Please note: A category is only displayed if it contains items.', verbose_name='Show category navigation')),
                ('category_navigation_all', models.BooleanField(default=False, help_text='If checked, a category "all" in filter navigation is displayed.', verbose_name='Show category "all"')),
                ('softpage_enabled', models.BooleanField(default=True, help_text='If checked, the detail view of an entry will be displayed in a "softpage". Otherwise the page will be reloaded.', verbose_name='Show detailed information in Softpage')),
                ('detail_link_enabled', models.BooleanField(default=True, help_text='If checked, a link/button to the detail view will be displayed.', verbose_name='Show detail link')),
                ('items_per_row', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], default=3, help_text='Only applied if a "Grid" template has been selected.', verbose_name='Grid items per row')),
                ('paginated_by', models.IntegerField(default=0, help_text='Limit the number of entries (in case of the "load more" pagination type: entries per page). Default is "0" (show all entries)', verbose_name='Max. entries per page')),
                ('pagination_type', models.CharField(choices=[('no', 'None'), ('load', 'Add "Load More"-Button')], default=('no', 'None'), max_length=50, verbose_name='Pagination Type')),
                ('load_more_button_text', models.CharField(blank=True, help_text='If left blank, a default text will be used. <br>Note: Should the default text be adjusted site-wide, please contact the project manager (such changes can be made on a code level)', max_length=255, null=True, verbose_name='Text for "Load More"-Button')),
                ('detail_link_text', models.CharField(blank=True, help_text='If left blank, a default text will be used.<br>Note: Should the default text be adjusted site-wide, please contact the project manager (such changes can be made on a code level)', max_length=255, null=True, verbose_name='Text for "Detail"-Link')),
                ('project_css_classes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None)),
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='testimonials_testimonialsappcontentplugin', serialize=False, to='cms.CMSPlugin')),
                ('categories', models.ManyToManyField(blank=True, to='allink_categories.AllinkCategory')),
                ('categories_and', models.ManyToManyField(blank=True, related_name='testimonials_testimonialsappcontentplugin_categories_and', to='allink_categories.AllinkCategory')),
                ('category_navigation', models.ManyToManyField(blank=True, help_text='You can explicitly define the categories for the category navigation here. This will override the automatically set of categories (either the one generated from "Filter & Ordering" or "Manual entries")', related_name='testimonials_testimonialsappcontentplugin_category_navigation', to='allink_categories.AllinkCategory', verbose_name='Categories for Navigation')),
                ('manual_entries', aldryn_common.admin_fields.sortedm2m.SortedM2MModelField(blank=True, help_text='Select and arrange specific entries, or, leave blank to select all. (If manual entries are selected the category filtering will be ignored.)', to='testimonials.Testimonials')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='TestimonialsTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('og_title', models.CharField(blank=True, help_text='Title when shared on Facebook.', max_length=255, null=True, verbose_name='Title Tag and Title when shared on Facebook/ Twitter.')),
                ('og_description', models.CharField(blank=True, help_text='Description when shared on Facebook/ Twitter.', max_length=255, null=True, verbose_name='Meta Description for Search Engines and when shared on Facebook.')),
                ('slug', models.SlugField(blank=True, default='', help_text='Leave blank to auto-generate a unique slug.', max_length=255, verbose_name='Slug')),
                ('lead', djangocms_text_ckeditor.fields.HTMLField(blank=True, help_text='Teaser text that in some cases is used in the list view and/or in the detail view.', null=True, verbose_name='Lead Text')),
                ('master', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='testimonials.Testimonials')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]