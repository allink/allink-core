# # -*- coding: utf-8 -*-
from django.urls import path

from allink_core.core.loading import get_class

TestimonialsPluginLoadMore = get_class('testimonials.views', 'TestimonialsPluginLoadMore')
TestimonialsDetail = get_class('testimonials.views', 'TestimonialsDetail')


urlpatterns = [
    path('<int:page>/', TestimonialsPluginLoadMore.as_view(), name='more'),
    path('<slug:slug>/', TestimonialsDetail.as_view(), name='detail'),
]
