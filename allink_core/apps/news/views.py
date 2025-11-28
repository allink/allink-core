# -*- coding: utf-8 -*-
from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView
from allink_core.core.loading import get_model

News = get_model('news', 'News')
Knowledge = get_model('news', 'Knowledge')

NewsAppContentPlugin = get_model('news', 'NewsAppContentPlugin')
KnowledgeAppContentPlugin = get_model('news', 'KnowledgeAppContentPlugin')


class NewsPluginLoadMore(AllinkBasePluginLoadMoreView):
    model = News
    plugin_model = NewsAppContentPlugin


class NewsDetail(AllinkBaseDetailView):
    model = News


class KnowledgePluginLoadMore(AllinkBasePluginLoadMoreView):
    model = Knowledge
    plugin_model = KnowledgeAppContentPlugin


class KnowledgeDetail(AllinkBaseDetailView):
    model = Knowledge
