# Generated by Django 2.1.8 on 2019-07-02 17:18

import allink_core.core.models.fields
import allink_core.core_apps.allink_button_link.model_fields
import cms.models.fields
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import djangocms_attributes_field.fields
import filer.fields.file
import filer.fields.image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('filer', '0011_auto_20190418_0137'),
        ('cms', '0022_auto_20180620_1551'),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkButtonLinkContainerPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='allink_button_link_allinkbuttonlinkcontainerplugin', serialize=False, to='cms.CMSPlugin')),
                ('alignment_horizontal_desktop', models.CharField(blank=True, choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], help_text='This option overrides the projects default alignment for desktop. (Usually "left")', max_length=50, null=True, verbose_name='Alignment horizontal desktop')),
                ('alignment_horizontal_mobile', models.CharField(blank=True, choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], help_text='This option overrides the projects default alignment for mobile. (Usually "left")', max_length=50, null=True, verbose_name='Alignment horizontal mobile')),
                ('project_css_classes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='AllinkButtonLinkPlugin',
            fields=[
                ('link_object_id', models.IntegerField(help_text='To which object directs the url.', null=True)),
                ('link_model', models.CharField(help_text='Dotted Path to referenced Model', max_length=300, null=True)),
                ('link_url_name', models.CharField(help_text='Name of the App-URL to use.', max_length=64, null=True)),
                ('link_url_kwargs', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, help_text='Keyword arguments used to reverse url.', null=True, size=None)),
                ('link_url', models.URLField(blank=True, default='', help_text='Provide a valid URL to an external website.', max_length=500, verbose_name='External link')),
                ('link_mailto', models.EmailField(blank=True, max_length=255, null=True, verbose_name='Email address')),
                ('link_phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Phone')),
                ('link_anchor', models.CharField(blank=True, help_text='Appends the value only after the internal or external link.<br>Do <strong>not</strong> include a preceding "#" symbol.', max_length=255, verbose_name='Anchor')),
                ('link_target', models.IntegerField(blank=True, choices=[(1, 'New window'), (2, 'Softpage (large)'), (3, 'Softpage (small)'), (4, 'Lightbox (Forms)'), (5, 'Lightbox (Image)'), (6, 'Lightbox (Default)')], null=True, verbose_name='Link Target')),
                ('link_special', models.CharField(blank=True, max_length=255, null=True, verbose_name='Special Links')),
                ('link_attributes', djangocms_attributes_field.fields.AttributesField(blank=True, default=dict, verbose_name='Attributes')),
                ('template', models.CharField(choices=[('default_link', 'Internal/External'), ('file_link', 'File (Download)'), ('image_link', 'Image'), ('phone_link', 'Phone'), ('email_link', 'Email'), ('form_link', 'Form'), ('video_embedded_link', 'Video (Embedded)'), ('video_file_link', 'Video (File)')], default='default_link', help_text='Choose a link type in order to display its options below.', max_length=50, verbose_name='Link type')),
                ('label', models.CharField(blank=True, default='', max_length=255, verbose_name='Link text')),
                ('type', allink_core.core_apps.allink_button_link.model_fields.LinkOrButton(default='lnk', max_length=255, verbose_name='Display type')),
                ('btn_context', allink_core.core_apps.allink_button_link.model_fields.Context(choices=[('default', 'Default'), ('primary', 'Primary'), ('success', 'Success'), ('info', 'Info'), ('warning', 'Warning'), ('danger', 'Danger'), ('link', 'Link')], default='default', max_length=255, verbose_name='Variation')),
                ('btn_size', allink_core.core_apps.allink_button_link.model_fields.Size(blank=True, default='md', max_length=255, verbose_name='Size')),
                ('btn_block', models.BooleanField(default=False, verbose_name='Block')),
                ('txt_context', allink_core.core_apps.allink_button_link.model_fields.Context(blank=True, choices=[('', 'Default'), ('primary', 'Primary'), ('success', 'Success'), ('info', 'Info'), ('warning', 'Warning'), ('danger', 'Danger'), ('muted ', 'Muted')], default='', max_length=255, verbose_name='Context')),
                ('icon_left', allink_core.core.models.fields.Icon(blank=True, default='', max_length=255, verbose_name='Icon left')),
                ('icon_right', allink_core.core.models.fields.Icon(blank=True, default='', max_length=255, verbose_name='Icon right')),
                ('email_subject', models.CharField(blank=True, default='', max_length=255, verbose_name='Subject')),
                ('email_body_text', models.TextField(blank=True, default='', verbose_name='Body Text')),
                ('send_internal_mail', models.BooleanField(default=False, help_text='Send confirmation mail to defined internal e-mail addresses.', verbose_name='Send internal e-mail')),
                ('internal_email_addresses', django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(blank=True, max_length=254, null=True), blank=True, null=True, size=None, verbose_name='Internal e-mail addresses')),
                ('from_email_address', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Sender e-mail address')),
                ('send_external_mail', models.BooleanField(default=False, help_text='Send confirmation mail to customer.', verbose_name='Send external e-mail')),
                ('thank_you_text', models.TextField(blank=True, help_text='This text will be shown, after form completion.', null=True, verbose_name='Thank you text')),
                ('label_layout', models.CharField(choices=[('stacked', 'Stacked with fields'), ('side_by_side', 'Side by side with fields'), ('placeholder', 'As placeholders')], default='stacked', max_length=15, verbose_name='Display labels')),
                ('project_css_classes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None)),
                ('video_id', models.CharField(blank=True, help_text='Only provide the ID. The correct URL will automatically be generated.<br><br>YouTube: https://www.youtube.com/watch?v=<strong>12345678</strong> (the ID is <strong>12345678</strong>)<br>Vimeo: https://vimeo.com/<strong>12345678</strong> (the ID is <strong>12345678</strong>)', max_length=255, null=True, verbose_name='Video ID')),
                ('video_service', models.CharField(blank=True, choices=[('youtube', 'Youtube'), ('vimeo', 'Vimeo')], max_length=50, null=True, verbose_name='Video Service')),
                ('ratio', models.CharField(blank=True, max_length=50, null=True, verbose_name='Ratio')),
                ('video_muted_enabled', models.BooleanField(default=True, help_text='Caution: Autoplaying videos with audio is not recommended. Use wisely.', verbose_name='Muted')),
                ('auto_start_enabled', models.BooleanField(default=False, help_text='<strong>Important:</strong> Autoplaying videos with audio is not recommended. Use wisely. ', verbose_name='Autostart')),
                ('allow_fullscreen_enabled', models.BooleanField(default=True, verbose_name='Allow fullscreen')),
                ('data_modal_escape_close_enabled', models.BooleanField(default=True, verbose_name='Escape key closes modal')),
                ('data_modal_overlay_close_enabled', models.BooleanField(default=True, verbose_name='Click on overlay closes modal')),
                ('data_modal_button_close_enabled', models.BooleanField(default=True, verbose_name='Display close button')),
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='allink_button_link_allinkbuttonlinkplugin', serialize=False, to='cms.CMSPlugin')),
                ('link_apphook_page', cms.models.fields.PageField(help_text='If provided, overrides the external link.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='allink_button_link_allinkbuttonlinkplugin_app_legacy_redirects', to='cms.Page', verbose_name='New Apphook-Page')),
                ('link_file', filer.fields.file.FilerFileField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='filer.File', verbose_name='file')),
                ('link_page', cms.models.fields.PageField(help_text='If provided, overrides the external link and New Apphook-Page.', null=True, on_delete=django.db.models.deletion.PROTECT, to='cms.Page', verbose_name='New Page')),
                ('video_file', filer.fields.file.FilerFileField(blank=True, help_text='Recommended video settings:<br><br>Format: mp4<br>Codec: H.264<br>Target Bitrate: 2 (video loads quick and runs smooth)<br>Audio: Not recommended (no audio = smaller file size and less annoyed visitors)<br>File size: Dependent of video length. Generally speaking: Less is more.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='allink_button_link_allinkbuttonlinkplugin_video_file', to='filer.File', verbose_name='Video File')),
                ('video_poster_image', filer.fields.image.FilerImageField(blank=True, help_text='Image that is being displayed while the video is loading. Ideally the very first frame of the video is used, in order to make the transition as smooth as possible.<br><br><strong>Imoprtant:</strong> Make sure the aspect ratio of the image is <strong>exactly the same</strong> as the video, otherwise the video height will shrink or grow when the playback starts.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='allink_button_link_allinkbuttonlinkplugin_video_poster_image', to=settings.FILER_IMAGE_MODEL, verbose_name='Video Start Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
    ]
