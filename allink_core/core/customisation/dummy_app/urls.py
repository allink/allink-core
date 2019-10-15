# # -*- coding: utf-8 -*-
from django.urls import path
from .views import TestAppPluginLoadMore, TestAppDetail


urlpatterns = [
    path('<int:page>/', TestAppPluginLoadMore.as_view(), name='more'),
    path('<slug:slug>/', TestAppDetail.as_view(), name='detail'),
]
