# # -*- coding: utf-8 -*-
from django.urls import path

from allink_core.core.loading import get_class


WorkPluginLoadMore = get_class('work.views', 'WorkPluginLoadMore')
WorkDetail = get_class('work.views', 'WorkDetail')
WorkSearchAjaxView = get_class('work.views', 'WorkSearchAjaxView')
export_pdf = get_class('work.views', 'export_pdf')


urlpatterns = [
    path('<int:page>/', WorkPluginLoadMore.as_view(), name='more'),
    path('<slug:slug>/', WorkDetail.as_view(), name='detail'),
    path('search/<int:plugin_id>/', WorkSearchAjaxView.as_view(), name='search'),
    path('export-pdf/<int:id>/', export_pdf, name='export-pdf'),
]
