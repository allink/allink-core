# -*- coding: utf-8 -*-
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.core.cms_toolbars import AllinkBaseModifierMixin
from .models import DummyApp


class DummyAppToolbar(AllinkBaseModifierMixin, CMSToolbar):
    model = DummyApp
    app_label = DummyApp._meta.app_label


toolbar_pool.register(DummyAppToolbar)
