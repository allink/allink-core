# -*- coding: utf-8 -*-
from allink_core.core.models.managers import AllinkCategoryModelQuerySet


class TestAppQuerySet(AllinkCategoryModelQuerySet):
    pass


TestAppManager = TestAppQuerySet.as_manager
