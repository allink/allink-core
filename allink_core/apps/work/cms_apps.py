# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class WorkApphook(CMSApp):
    name = _("Work Apphook")
    app_name = 'work'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['allink_core.apps.work.urls']


apphook_pool.register(WorkApphook)
