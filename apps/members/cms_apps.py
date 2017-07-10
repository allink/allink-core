# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class MembersApphook(CMSApp):
    name = _("Members Apphook")
    app_name = 'members'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['allink_apps.members.urls']


apphook_pool.register(MembersApphook)
