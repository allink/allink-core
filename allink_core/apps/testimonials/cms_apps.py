# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class TestimonialsApphook(CMSApp):
    name = "Testimonials Apphook"
    app_name = 'testimonials'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['allink_core.apps.testimonials.urls']


apphook_pool.register(TestimonialsApphook)
