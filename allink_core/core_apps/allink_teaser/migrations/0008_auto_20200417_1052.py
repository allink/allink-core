# Generated by Django 2.2.12 on 2020-04-17 10:52

from django.db import migrations


def set_new_default_value(apps, schema_editor):
    AllinkTeaserPlugin = apps.get_model('allink_teaser', 'AllinkTeaserPlugin')
    for teaser in AllinkTeaserPlugin.objects.all():
        if teaser.softpage_enabled:
            teaser.link_target = 2
            teaser.save()


class Migration(migrations.Migration):

    dependencies = [
        ('allink_teaser', '0007_allinkteaserplugin_link_target'),
    ]

    operations = [
        migrations.RunPython(set_new_default_value),
    ]
