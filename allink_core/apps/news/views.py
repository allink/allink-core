# -*- coding: utf-8 -*-
from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView
from allink_core.core.loading import get_model

News = get_model('news', 'News')
NewsAppContentPlugin = get_model('news', 'NewsAppContentPlugin')


class NewsPluginLoadMore(AllinkBasePluginLoadMoreView):
    model = News
    plugin_model = NewsAppContentPlugin


class NewsDetail(AllinkBaseDetailView):
    model = News
