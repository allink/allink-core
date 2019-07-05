# # -*- coding: utf-8 -*-
from django.urls import path
from allink_core.core.loading import get_class

EventsPluginLoadMore = get_class('events.views', 'EventsPluginLoadMore')
EventsDetail = get_class('events.views', 'EventsDetail')
EventsRegistrationView = get_class('events.views', 'EventsRegistrationView')


urlpatterns = [
    path('<int:page>/', EventsPluginLoadMore.as_view(), name='more'),
    path('<slug:slug>/', EventsDetail.as_view(), name='detail'),
    path('<slug:slug>/register/', EventsRegistrationView.as_view(), name='register'),
]
