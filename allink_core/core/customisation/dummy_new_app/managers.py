# -*- coding: utf-8 -*-
from allink_core.core.models.managers import AllinkCategoryModelQuerySet


class DummyAppQuerySet(AllinkCategoryModelQuerySet):
    pass


DummyAppManager = DummyAppQuerySet.as_manager
