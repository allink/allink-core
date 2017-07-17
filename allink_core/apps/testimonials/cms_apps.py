# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class TestimonialsApphook(CMSApp):
    name = _("Testimonials Apphook")
    app_name = 'testimonials'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['allink_core.apps.testimonials.urls']


apphook_pool.register(TestimonialsApphook)
