# -*- coding: utf-8 -*-
from allink_core.core.models.managers import AllinkCategoryModelQuerySet


class AllinkWorkQuerySet(AllinkCategoryModelQuerySet):
    pass


AllinkWorkManager = AllinkWorkQuerySet.as_manager
