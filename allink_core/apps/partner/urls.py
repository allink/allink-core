# # -*- coding: utf-8 -*-
from django.urls import path
from .views import PartnerPluginLoadMore, PartnerDetail


urlpatterns = [
    path('<int:page>/', PartnerPluginLoadMore.as_view(), name='more'),
    path('<slug:slug>/', PartnerDetail.as_view(), name='detail'),
]
