# # -*- coding: utf-8 -*-
from django.urls import path

from allink_core.core.loading import get_class

PeoplePluginLoadMore = get_class('people.views', 'PeoplePluginLoadMore')
PeopleDetail = get_class('people.views', 'PeopleDetail')


urlpatterns = [
    path('<int:page>/', PeoplePluginLoadMore.as_view(), name='more'),
    path('<slug:slug>/', PeopleDetail.as_view(), name='detail'),
]
