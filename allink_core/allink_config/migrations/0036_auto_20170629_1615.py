# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import activate
from django.db import migrations, models
from django.conf import settings


def translate_meta_fields(apps, schema_editor):
    AllinkConfig = apps.get_model('allink_config', 'AllinkConfig')
    AllinkConfigTranslation = apps.get_model('allink_config', 'AllinkConfigTranslation')
    language_code = settings.LANGUAGES[0][0]
    activate(language_code)

    for b in AllinkConfig.objects.all():
        translation = _get_translation(b, AllinkConfigTranslation)
        translation.default_base_title = b.old_default_base_title
        translation.save(update_fields=['default_base_title'])


def _get_translation(obj, translation_class):
    translations = translation_class.objects.filter(master_id=obj.pk)
    language_code = settings.LANGUAGES[0][0]
    try:
        return translations.get(language_code=language_code)
    except translation_class.DoesNotExist:
        try:
            return translations.get()
        except:
            translation_class.objects.create(master_id=obj.pk, language_code=language_code, default_base_title='')
            return translations.get(language_code=language_code)


class Migration(migrations.Migration):

    dependencies = [
        ('allink_config', '0035_auto_20170629_1416'),
    ]

    operations = [
        migrations.RunPython(translate_meta_fields)
    ]
