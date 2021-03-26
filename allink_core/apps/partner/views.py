# -*- coding: utf-8 -*-
from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView
from .models import Partner, PartnerAppContentPlugin


class PartnerPluginLoadMore(AllinkBasePluginLoadMoreView):
    model = Partner
    plugin_model = PartnerAppContentPlugin


class PartnerDetail(AllinkBaseDetailView):
    model = Partner
