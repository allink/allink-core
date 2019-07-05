# -*- coding: utf-8 -*-
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.core.cms_toolbars import AllinkBaseModifierMixin
from allink_core.core.loading import get_model

Config = get_model('config', 'Config')
Work = get_model('work', 'Work')


class WorkToolbar(AllinkBaseModifierMixin, CMSToolbar):
    model = Work
    app_label = Work._meta.app_label


toolbar_pool.register(WorkToolbar)
