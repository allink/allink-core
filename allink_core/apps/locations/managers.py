# -*- coding: utf-8 -*-
from allink_core.core.models.managers import AllinkCategoryModelQuerySet


class AllinkLocationsQuerySet(AllinkCategoryModelQuerySet):
    pass


AllinkLocationsManager = AllinkLocationsQuerySet.as_manager
