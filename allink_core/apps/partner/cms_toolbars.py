# -*- coding: utf-8 -*-
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.core.cms_toolbars import AllinkBaseModifierMixin
from allink_core.core.loading import get_model

Partner = get_model('partner', 'Partner')


class PartnerToolbar(AllinkBaseModifierMixin, CMSToolbar):
    model = Partner
    app_label = Partner._meta.app_label


toolbar_pool.register(PartnerToolbar)
