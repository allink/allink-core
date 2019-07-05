# Generated by Django 2.1.8 on 2019-07-02 17:18

import adminsortable.fields
import cms.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms', '0022_auto_20180620_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkLanguageChooserPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='allink_cms_allinklanguagechooserplugin', serialize=False, to='cms.CMSPlugin')),
            ],
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='AllinkPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('just_descendants', models.BooleanField(default=False, help_text='If checked and pages selected manually, only the descendants of the selected pages will be listed.', verbose_name='Select just descendants')),
                ('page', cms.models.fields.PageField(on_delete=django.db.models.deletion.CASCADE, to='cms.Page')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
        ),
        migrations.CreateModel(
            name='AllinkPageChooserPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='allink_cms_allinkpagechooserplugin', serialize=False, to='cms.CMSPlugin')),
            ],
            bases=('cms.cmsplugin',),
        ),
        migrations.AddField(
            model_name='allinkpage',
            name='pagechooser',
            field=adminsortable.fields.SortableForeignKey(blank=True, help_text='Add pages and order them.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='allink_cms.AllinkPageChooserPlugin', verbose_name='Images'),
        ),
    ]
