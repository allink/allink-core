# # -*- coding: utf-8 -*-
from django.conf.urls import url

from allink_core.core.loading import get_class

WorkPluginLoadMore = get_class('work.views', 'WorkPluginLoadMore')
WorkDetail = get_class('work.views', 'WorkDetail')
WorkSearchAjaxView = get_class('work.views', 'WorkSearchAjaxView')
export_pdf = get_class('work.views', 'export_pdf')


urlpatterns = [
    url(r'^(?P<page>[0-9]*)/$', WorkPluginLoadMore.as_view(), name='more'),
    url(r'^(?P<slug>[\w-]+)/$', WorkDetail.as_view(), name='detail'),
    url(r'^search/(?P<plugin_id>[0-9]+)/$', WorkSearchAjaxView.as_view(), name='search'),
    url(r'^export-pdf/(?P<id>[0-9]+)/$', export_pdf, name='export-pdf'),
]
