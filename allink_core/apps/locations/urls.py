# # -*- coding: utf-8 -*-
from django.urls import path

from allink_core.core.loading import get_class

LocationsPluginLoadMore = get_class('locations.views', 'LocationsPluginLoadMore')
LocationsDetail = get_class('locations.views', 'LocationsDetail')
export_pdf = get_class('locations.views', 'export_pdf')


urlpatterns = [
    path('<int:page>/', LocationsPluginLoadMore.as_view(), name='more'),
    path('<slug:slug>/', LocationsDetail.as_view(), name='detail'),
    path('export-pdf/<int:id>/', export_pdf, name='export-pdf'),
]
