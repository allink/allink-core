# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.file
import allink_core.djangocms_button_link.model_fields
import django.db.models.deletion
import cms.models.fields
import djangocms_attributes_field.fields
import allink_core.allink_base.models.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('filer', '0006_auto_20160623_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkButtonLinkContainerPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_button_link_allinkbuttonlinkcontainerplugin', auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='AllinkButtonLinkPlugin',
            fields=[
                ('link_url', models.URLField(default=b'', help_text='Provide a valid URL to an external website.', verbose_name='External link', blank=True)),
                ('link_mailto', models.EmailField(max_length=255, null=True, verbose_name='Email address', blank=True)),
                ('link_phone', models.CharField(max_length=255, null=True, verbose_name='Phone', blank=True)),
                ('link_anchor', models.CharField(help_text='Appends the value only after the internal or external link. Do <em>not</em> include a preceding "#" symbol.', max_length=255, verbose_name='Anchor', blank=True)),
                ('link_target', models.BooleanField(verbose_name='Open in new Window')),
                ('link_attributes', djangocms_attributes_field.fields.AttributesField(default=dict, verbose_name='Attributes', blank=True)),
                ('title', models.CharField(default=b'', max_length=255, verbose_name='Display name', blank=True)),
                ('type', allink_core.djangocms_button_link.model_fields.LinkOrButton(default='lnk', max_length=255, verbose_name='Type')),
                ('btn_context', allink_core.djangocms_button_link.model_fields.Context(default=b'default', max_length=255, verbose_name='Context', choices=[(b'default', b'Default'), (b'primary', b'Primary'), (b'success', b'Success'), (b'info', b'Info'), (b'warning', b'Warning'), (b'danger', b'Danger'), (b'link', b'Link')])),
                ('btn_size', allink_core.djangocms_button_link.model_fields.Size(default='md', max_length=255, verbose_name='Size', blank=True)),
                ('btn_block', models.BooleanField(default=False, verbose_name='Block')),
                ('txt_context', allink_core.djangocms_button_link.model_fields.Context(default=b'', max_length=255, verbose_name='Context', blank=True, choices=[(b'', b'Default'), (b'primary', b'Primary'), (b'success', b'Success'), (b'info', b'Info'), (b'warning', b'Warning'), (b'danger', b'Danger'), (b'muted ', b'Muted')])),
                ('icon_left', allink_core.allink_base.models.model_fields.Icon(default=b'', max_length=255, verbose_name='Icon left', blank=True)),
                ('icon_right', allink_core.allink_base.models.model_fields.Icon(default=b'', max_length=255, verbose_name='Icon right', blank=True)),
                ('extra_css_classes', allink_core.allink_base.models.model_fields.Classes(default=b'', help_text='Space separated classes that are added to the class. See <a href="http://getbootstrap.com/css/" target="_blank">Bootstrap 3 documentation</a>.', verbose_name='Classes', blank=True)),
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_button_link_allinkbuttonlinkplugin', primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('link_file', filer.fields.file.FilerFileField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='file', blank=True, to='filer.File', null=True)),
                ('link_page', cms.models.fields.PageField(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='cms.Page', help_text='If provided, overrides the external link.', null=True, verbose_name='Internal link')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
    ]
