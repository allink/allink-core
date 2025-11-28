# -*- coding: utf-8 -*-
from django.urls import path
from allink_core.core.loading import get_class

KnowledgePluginLoadMore = get_class('news.views', 'KnowledgePluginLoadMore')
KnowledgeDetail = get_class('news.views', 'KnowledgeDetail')

app_name='knowledge'
urlpatterns = [
    path('<int:page>/', KnowledgePluginLoadMore.as_view(), name='more'),
    path('<slug:slug>/', KnowledgeDetail.as_view(), name='detail'),
]
