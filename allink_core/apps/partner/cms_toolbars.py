# -*- coding: utf-8 -*-
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.core.cms_toolbars import AllinkBaseModifierMixin
from .models import Partner


class PartnerToolbar(AllinkBaseModifierMixin, CMSToolbar):
    model = Partner
    app_label = Partner._meta.app_label


toolbar_pool.register(PartnerToolbar)
