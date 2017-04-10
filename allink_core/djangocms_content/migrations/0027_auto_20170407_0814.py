# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import allink_core.allink_base.models.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_content', '0026_allinkcontentplugin_anchor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allinkcontentcolumnplugin',
            name='alignment_horizontal_desktop',
            field=models.CharField(null=True, blank=True, max_length=50, choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], verbose_name='Alignment horizontal desktop', help_text='This option overrides the projects default alignment for desktop. (Usually "left")'),
        ),
        migrations.AlterField(
            model_name='allinkcontentcolumnplugin',
            name='alignment_horizontal_mobile',
            field=models.CharField(null=True, blank=True, max_length=50, choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], verbose_name='Alignment horizontal mobile', help_text='This option overrides the projects default alignment for mobile. (Usually "left")'),
        ),
        migrations.AlterField(
            model_name='allinkcontentcolumnplugin',
            name='alignment_vertical_desktop',
            field=models.CharField(null=True, blank=True, max_length=50, choices=[('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom')], verbose_name='Alignment vertical desktop', help_text='This option overrides the projects default alignment for desktop. (Usually "top")'),
        ),
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='extra_css_classes',
            field=allink_core.allink_base.models.model_fields.Classes(default='', blank=True, verbose_name='Css Classes', help_text='Space separated classes that are added to the list of classes.'),
        ),
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='title_size',
            field=models.CharField(default='h1', max_length=50, choices=[('h1', 'Title Large'), ('h2', 'Title Medium')], verbose_name='Section Title Size'),
        ),
        migrations.AlterField(
            model_name='allinkcontentplugin',
            name='video_mobile_image_alignment',
            field=models.CharField(default='center', max_length=50, choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')], verbose_name='Mobile Image Alignment (horizontal)', help_text='TBD Define which part of the image must be visible. Because we use the available space, there is a chance that a part (left and/or right) is not visible.'),
        ),
    ]
