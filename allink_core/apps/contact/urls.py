# # -*- coding: utf-8 -*-
from django.urls import path
from allink_core.core.loading import get_class

ContactRequestView = get_class('contact.views', 'ContactRequestView')


urlpatterns = [
    path('request/<int:plugin_id>/', ContactRequestView.as_view(), name='request'),
]
