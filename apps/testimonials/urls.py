# # -*- coding: utf-8 -*-
from django.conf.urls import url

from allink_core.core.loading import get_class

TestimonialsPluginLoadMore = get_class('testimonials.views', 'TestimonialsPluginLoadMore')
TestimonialsDetail = get_class('testimonials.views', 'TestimonialsDetail')


urlpatterns = [
    url(r'^(?P<page>[0-9]*)/$', TestimonialsPluginLoadMore.as_view(), name='more'),
    url(r'^(?P<slug>[\w-]+)/$', TestimonialsDetail.as_view(), name='detail'),
]
