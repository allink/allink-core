# -*- coding: utf-8 -*-
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.core.cms_toolbars import AllinkBaseModifierMixin
from allink_core.core.loading import get_model

News = get_model('news', 'News')

Config = get_model('config', 'Config')
config = Config.get_solo()


class NewsToolbar(AllinkBaseModifierMixin, CMSToolbar):
    model = News
    app_label = News._meta.app_label


if getattr(config, 'news_toolbar_enabled', True):
    toolbar_pool.register(NewsToolbar)