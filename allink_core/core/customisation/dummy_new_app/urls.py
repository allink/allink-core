# # -*- coding: utf-8 -*-
from django.urls import path
from .views import DummyAppPluginLoadMore, DummyAppDetail


urlpatterns = [
    path('<int:page>/', DummyAppPluginLoadMore.as_view(), name='more'),
    path('<slug:slug>/', DummyAppDetail.as_view(), name='detail'),
]
