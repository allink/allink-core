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


if getattr(Config.get_solo(), 'work_toolbar_enabled', True):
    toolbar_pool.register(WorkToolbar)
