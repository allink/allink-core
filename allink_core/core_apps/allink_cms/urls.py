# # -*- coding: utf-8 -*-
from django.urls import path

from allink_core.core_apps.allink_cms.api import CMSPluginAPIView


# TODO this is only the beginning
# we will add a complete api for pages/ placeholders/ plugins etc. (preferably as json)
app_name = 'allink_cms'

urlpatterns = [
    path('plugins/<int:id>/', CMSPluginAPIView.as_view(), name='plugins'),
]
