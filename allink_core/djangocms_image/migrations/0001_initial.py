# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.file
import django.db.models.deletion
import filer.fields.image
import cms.models.fields
import djangocms_attributes_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0016_auto_20160608_1535'),
        ('filer', '0006_auto_20160623_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkImagePlugin',
            fields=[
                ('link_url', models.URLField(default=b'', help_text='Provide a valid URL to an external website.', verbose_name='External link', blank=True)),
                ('link_mailto', models.EmailField(max_length=255, null=True, verbose_name='Email address', blank=True)),
                ('link_phone', models.CharField(max_length=255, null=True, verbose_name='Phone', blank=True)),
                ('link_anchor', models.CharField(help_text='Appends the value only after the internal or external link. Do <em>not</em> include a preceding "#" symbol.', max_length=255, verbose_name='Anchor', blank=True)),
                ('link_target', models.BooleanField(verbose_name='Open in new Window')),
                ('link_special', models.CharField(blank=True, max_length=255, null=True, verbose_name='Special Links', choices=[(b'account_login', 'Member Login'), (b'account_logout', 'Member Logout'), (b'account_change_password', 'Member Change Passwort'), (b'account_reset_password', 'Member Reset Passwort'), (b'members:profile_edit', 'Member Edit Profile')])),
                ('link_attributes', djangocms_attributes_field.fields.AttributesField(default=dict, verbose_name='Attributes', blank=True)),
                ('template', models.CharField(default=(b'default', b'Default'), help_text='Choose a template.', max_length=50, verbose_name='Template', choices=[(b'default', b'Default')])),
                ('external_picture', models.URLField(help_text='If provided, overrides the embedded image. Certain options such as cropping are not applicable to external images.', max_length=255, verbose_name='External image', blank=True)),
                ('caption_text', models.TextField(help_text='Provide a description, attribution, copyright or other information.', verbose_name='Caption text', blank=True)),
                ('attributes', djangocms_attributes_field.fields.AttributesField(default=dict, verbose_name='Attributes', blank=True)),
                ('width', models.PositiveIntegerField(help_text='The image width as number in pixels. Example: "720" and not "720px".', null=True, verbose_name='Width', blank=True)),
                ('use_no_cropping', models.BooleanField(default=False, help_text='Outputs the raw image without cropping.', verbose_name='Use original image')),
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='djangocms_image_allinkimageplugin', primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('link_file', filer.fields.file.FilerFileField(verbose_name='file', blank=True, to='filer.File', null=True)),
                ('link_page', cms.models.fields.PageField(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='cms.Page', help_text='If provided, overrides the external link.', null=True, verbose_name='Internal link')),
                ('picture', filer.fields.image.FilerImageField(related_name='djangocms_image_allinkimageplugin_picture', on_delete=django.db.models.deletion.SET_NULL, verbose_name='Image', blank=True, to='filer.Image', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
    ]
