# -*- coding: utf-8 -*-
from django.db import models

from allink_core.core.models.base_plugins import AllinkBaseSectionPlugin


class AllinkSectionPlugin(AllinkBaseSectionPlugin):
    COLUMNS = (
        ('1-of-1', 'One Column'),
    )
