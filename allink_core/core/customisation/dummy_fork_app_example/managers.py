# -*- coding: utf-8 -*-
"""
use core:
from allink_core.apps.dummy_app.managers import *  # noqa
"""
from allink_core.apps.dummy_app.managers import AllinkDummyAppQuerySet


class AllinkDummyAppQuerySet(AllinkDummyAppQuerySet):
    def new(self):
        return self.filter(status=1)


AllinkDummyAppManager = AllinkDummyAppQuerySet.as_manager
