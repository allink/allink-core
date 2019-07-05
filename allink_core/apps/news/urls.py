# -*- coding: utf-8 -*-
from django.urls import path
from allink_core.core.loading import get_class

NewsPluginLoadMore = get_class('news.views', 'NewsPluginLoadMore')
NewsDetail = get_class('news.views', 'NewsDetail')

urlpatterns = [
    path('<int:page>/', NewsPluginLoadMore.as_view(), name='more'),
    path('<slug:slug>/', NewsDetail.as_view(), name='detail'),
]
