# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class PartnerApphook(CMSApp):
    name = _("Partner Apphook")
    app_name = 'partner'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['allink_core.apps.partner.urls']


apphook_pool.register(PartnerApphook)
