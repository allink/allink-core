# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('filer', '0006_auto_20160623_1627'),
        ('djangocms_content', '0019_auto_20161204_0943'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkContentColumnPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_content_allinkcontentcolumnplugin', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title', blank=True)),
                ('template', models.CharField(default=b'col-1', max_length=50, verbose_name='Template', choices=[(b'col-1', b'1 Column'), (b'col-1-1', b'2 Columns (1:1)'), (b'col-2-1', b'2 Columns (2:1)'), (b'col-1-2', b'2 Columns (1:2)'), (b'col-3', b'3 Columns')])),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='AllinkContentPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_content_allinkcontentplugin', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(help_text='The section title', max_length=255, null=True, verbose_name='Title', blank=True)),
                ('template', models.CharField(default=(b'col-1', b'1 Column'), help_text='Choose a template. This settings can NOT be changed after the content has been saved.', max_length=50, verbose_name='Template', choices=[(b'col-1', b'1 Column'), (b'col-1-1', b'2 Columns (1:1)'), (b'col-2-1', b'2 Columns (2:1)'), (b'col-1-2', b'2 Columns (1:2)'), (b'col-3', b'3 Columns')])),
                ('container_enabled', models.BooleanField(default=True, help_text='If checked, an inner container with a maximum width is added', verbose_name='Display columns within container')),
                ('bg_color', models.IntegerField(blank=True, null=True, verbose_name='Set a predefined background color', choices=[(0, b'#000000'), (1, b'#373a3c'), (2, b'#373a3c')])),
                ('overlay_styles_enabled', models.BooleanField(default=False, help_text='If checked, the predefined overlay styles are applied (suitable when text is over an image/video)', verbose_name='Activate overlay styles')),
                ('parallax_enabled', models.BooleanField(default=False, help_text='TBD: Disable until background image is set.', verbose_name='Activate Parallax effect')),
                ('extra_css_classes', models.CharField(help_text='Comma separated class names. Only letters, numbers, hyphen and underscores are allowed in class names.', max_length=255, null=True, verbose_name='CSS Classes', blank=True)),
                ('bg_image_inner_container', filer.fields.image.FilerImageField(related_name='content_container_bg_image', blank=True, to='filer.Image', help_text='Dimensions TBD', null=True, verbose_name='Background-Image (Inner Container)')),
                ('bg_image_outer_container', filer.fields.image.FilerImageField(related_name='content_bg_image', blank=True, to='filer.Image', help_text='Dimensions TBD', null=True, verbose_name='Background-Image (Outer Container)')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.RemoveField(
            model_name='allinkcontent',
            name='bg_image_inner_container',
        ),
        migrations.RemoveField(
            model_name='allinkcontent',
            name='bg_image_outer_container',
        ),
        migrations.RemoveField(
            model_name='allinkcontent',
            name='cmsplugin_ptr',
        ),
        migrations.RemoveField(
            model_name='allinkcontentcolumn',
            name='cmsplugin_ptr',
        ),
        migrations.DeleteModel(
            name='AllinkContent',
        ),
        migrations.DeleteModel(
            name='AllinkContentColumn',
        ),
    ]
