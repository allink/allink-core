# -*- coding: utf-8 -*-
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.core.cms_toolbars import AllinkBaseModifierMixin
from allink_core.core.loading import get_model

Config = get_model('config', 'Config')
Testimonials = get_model('testimonials', 'Testimonials')


class TestimonialsToolbar(AllinkBaseModifierMixin, CMSToolbar):
    model = Testimonials
    app_label = Testimonials._meta.app_label


toolbar_pool.register(TestimonialsToolbar)
