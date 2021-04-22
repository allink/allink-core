# -*- coding: utf-8 -*-
from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView
from allink_core.core.loading import get_model

Partner = get_model('partner', 'Partner')
PartnerAppContentPlugin = get_model('partner', 'PartnerAppContentPlugin')


class PartnerPluginLoadMore(AllinkBasePluginLoadMoreView):
    model = Partner
    plugin_model = PartnerAppContentPlugin


class PartnerDetail(AllinkBaseDetailView):
    model = Partner
