# -*- coding: utf-8 -*-
from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView
from allink_core.core.loading import get_model


Testimonials = get_model('testimonials', 'Testimonials')
TestimonialsAppContentPlugin = get_model('testimonials', 'TestimonialsAppContentPlugin')


class TestimonialsPluginLoadMore(AllinkBasePluginLoadMoreView):
    model = Testimonials
    plugin_model = TestimonialsAppContentPlugin


class TestimonialsDetail(AllinkBaseDetailView):
    model = Testimonials
