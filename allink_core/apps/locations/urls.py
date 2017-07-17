# # -*- coding: utf-8 -*-
from django.conf.urls import url

from allink_core.core.loading import get_class

LocationsPluginLoadMore = get_class('locations.views', 'LocationsPluginLoadMore')
LocationsDetail = get_class('locations.views', 'LocationsDetail')
export_pdf = get_class('locations.views', 'export_pdf')


urlpatterns = [
    url(r'^(?P<page>[0-9]*)/$', LocationsPluginLoadMore.as_view(), name='more'),
    url(r'^(?P<slug>[\w-]+)/$', LocationsDetail.as_view(), name='detail'),
    url(r'^export-pdf/(?P<id>[0-9]+)/$', export_pdf, name='export-pdf'),
]
