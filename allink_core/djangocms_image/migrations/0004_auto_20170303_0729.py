# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import connection
from django.db import migrations, models


def delete_old_plugin(apps, schema_editor):

    OldPlugin = apps.get_model("djangocms_picture", "Picture")

    cursor = connection.cursor()
    table_name = OldPlugin._meta.db_table
    sql = "DROP TABLE %s;" % (table_name, )
    cursor.execute(sql)


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_image', '0003_auto_20170302_0455'),
        ('djangocms_picture', '0007_fix_alignment'),
    ]

    operations = [
        migrations.RunPython(delete_old_plugin),
    ]
