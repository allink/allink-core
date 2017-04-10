# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils.translation import activate


def set_root_category_model_names(apps, schema_editor):
    from allink_core.allink_categories.models import AllinkCategory
    activate('de')

    if AllinkCategory.get_root_nodes():
        for root in AllinkCategory.get_root_nodes():
            collected_model_names = []
            for child in root.get_children():
                if child.model_names:
                    for model_name in child.model_names:
                        # add the model_name if not already added
                        if model_name not in collected_model_names:
                            collected_model_names.append(model_name)

            # now add to root.model_names but keep the names which are already there
            to_add = root.model_names if root.model_names else []

            if collected_model_names:
                for model_name in collected_model_names:
                    # add the model_name if not already added
                    if model_name not in to_add:
                        to_add.append(model_name)
                root.model_names = to_add
                root.save()



class Migration(migrations.Migration):

    dependencies = [
        ('allink_categories', '0017_auto_20170403_0409'),
    ]

    operations = [
        migrations.RunPython(set_root_category_model_names),
    ]
