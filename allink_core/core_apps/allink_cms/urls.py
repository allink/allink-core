# # -*- coding: utf-8 -*-
from django.conf.urls import url

from allink_core.core_apps.allink_cms.api import CMSPluginAPIView

# TODO this is only the beginning
# we will add a complete api for pages/ placeholders/ plugins etc. (preferably as json)
urlpatterns = [
    url(r'plugins/(?P<id>[0-9]*)/$', CMSPluginAPIView.as_view(), name='plugins'),
]
