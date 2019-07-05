# -*- coding: utf-8 -*-
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.core.cms_toolbars import AllinkBaseModifierMixin
from allink_core.core.loading import get_model

News = get_model('news', 'News')


class NewsToolbar(AllinkBaseModifierMixin, CMSToolbar):
    model = News
    app_label = News._meta.app_label


toolbar_pool.register(NewsToolbar)
