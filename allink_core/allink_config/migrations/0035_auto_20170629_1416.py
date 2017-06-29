# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0034_allinkmetatagextension_disable_base_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllinkConfigTranslation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('language_code', models.CharField(max_length=15, db_index=True, verbose_name='Language')),
                ('default_base_title', models.CharField(max_length=50, null=True, verbose_name='Base title', blank=True, help_text='Default base title, Is also used for default base og:title when page/post is shared on Facebook. <br>If not supplied the name form Django Sites will be used instead.')),
            ],
            options={
                'managed': True,
                'db_table': 'allink_config_allinkconfig_translation',
                'default_permissions': (),
                'db_tablespace': '',
                'verbose_name': 'Allink Configuration Translation',
            },
        ),
        migrations.RenameField(
            model_name='allinkconfig',
            old_name='default_base_title',
            new_name='old_default_base_title',
        ),
        migrations.AddField(
            model_name='allinkconfigtranslation',
            name='master',
            field=models.ForeignKey(to='allink_config.AllinkConfig', null=True, related_name='translations', editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='allinkconfigtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
