# Generated by Django 2.2.16 on 2021-03-25 16:23

import cms.models.fields
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import djangocms_attributes_field.fields
import filer.fields.file


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0012_file_mime_type'),
        ('cms', '0022_auto_20180620_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkImageSVGPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='allink_image_svg_allinkimagesvgplugin', serialize=False, to='cms.CMSPlugin')),
                ('link_object_id', models.IntegerField(help_text='To which object directs the url.', null=True)),
                ('link_model', models.CharField(help_text='Dotted Path to referenced Model', max_length=300, null=True)),
                ('link_url_name', models.CharField(help_text='Name of the App-URL to use.', max_length=64, null=True)),
                ('link_url_kwargs', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, help_text='Keyword arguments used to reverse url.', null=True, size=None)),
                ('link_url', models.URLField(blank=True, default='', help_text='Provide a valid URL to an external website.', max_length=500, verbose_name='External link')),
                ('link_mailto', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email address')),
                ('link_phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Phone')),
                ('link_anchor', models.CharField(blank=True, help_text='Appends the value only after the internal or external link.<br>Do <strong>not</strong> include a preceding "#" symbol.', max_length=255, verbose_name='Anchor')),
                ('link_target', models.IntegerField(blank=True, choices=[(1, 'New window'), (2, 'Softpage'), (4, 'Lightbox (Forms)'), (5, 'Lightbox (Image)'), (6, 'Lightbox (Default)')], null=True, verbose_name='Link Target')),
                ('link_special', models.CharField(blank=True, max_length=255, null=True, verbose_name='Special Links')),
                ('link_attributes', djangocms_attributes_field.fields.AttributesField(blank=True, default=dict, verbose_name='Attributes')),
                ('is_inline', models.BooleanField(default=False, help_text='Check if the SVG should be inlined.', verbose_name='Is inline')),
                ('link_apphook_page', cms.models.fields.PageField(help_text='If provided, overrides the external link.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='allink_image_svg_allinkimagesvgplugin_app_legacy_redirects', to='cms.Page', verbose_name='New Apphook-Page')),
                ('link_file', filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='filer.File', verbose_name='file')),
                ('link_page', cms.models.fields.PageField(help_text='If provided, overrides the external link and New Apphook-Page.', null=True, on_delete=django.db.models.deletion.PROTECT, to='cms.Page', verbose_name='New Page')),
                ('picture', filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='allink_image_svg_allinkimagesvgplugin_image', to='filer.File', verbose_name='Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
    ]
