# # -*- coding: utf-8 -*-
from django.urls import path
from .views import PartnerPluginLoadMore, PartnerDetail

from allink_core.core.loading import get_class

PeoplePluginLoadMore = get_class('people.views', 'PeoplePluginLoadMore')
PeopleDetail = get_class('people.views', 'PeopleDetail')

urlpatterns = [
    path('<int:page>/', PartnerPluginLoadMore.as_view(), name='more'),
    path('<slug:slug>/', PartnerDetail.as_view(), name='detail'),
]
