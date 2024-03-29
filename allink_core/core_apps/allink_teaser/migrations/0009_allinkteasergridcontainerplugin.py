# Generated by Django 2.2.16 on 2021-03-25 12:21

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
        ('allink_teaser', '0008_auto_20201102_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkTeaserGridContainerPlugin',
            fields=[
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title')),
                ('columns', models.CharField(help_text='Choose columns.', max_length=50, verbose_name='Columns')),
                ('column_order', models.CharField(help_text='Choose a column order.', max_length=50, verbose_name='Column Order')),
                ('anchor', models.CharField(blank=True, help_text='ID of this content section which can be used for anchor reference from links.<br>Note: Only letters, numbers and hyphen. No spaces or special chars.', max_length=255, verbose_name='ID')),
                ('project_css_classes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=50, null=True), blank=True, null=True, size=None)),
                ('project_css_spacings_top_bottom', models.CharField(blank=True, help_text='Choose a spacing (top and bottom).', max_length=50, null=True, verbose_name='Spacings')),
                ('project_css_spacings_top', models.CharField(blank=True, help_text='Choose a top spacing.', max_length=50, null=True, verbose_name='Spacings top')),
                ('project_css_spacings_bottom', models.CharField(blank=True, help_text='Choose a bottom spacing.', max_length=50, null=True, verbose_name='Spacings bottom')),
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='allink_teaser_allinkteasergridcontainerplugin', serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
