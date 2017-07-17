# # -*- coding: utf-8 -*-
from django.conf.urls import url

from allink_core.core.loading import get_class

PeoplePluginLoadMore = get_class('people.views', 'PeoplePluginLoadMore')
PeopleDetail = get_class('people.views', 'PeopleDetail')


urlpatterns = [
    url(r'^(?P<page>[0-9]*)/$', PeoplePluginLoadMore.as_view(), name='more'),
    url(r'^(?P<slug>[\w-]+)/$', PeopleDetail.as_view(), name='detail'),
]
