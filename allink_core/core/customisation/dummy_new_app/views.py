# -*- coding: utf-8 -*-
from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView
from .models import DummyApp, DummyAppAppContentPlugin


class DummyAppPluginLoadMore(AllinkBasePluginLoadMoreView):
    model = DummyApp
    plugin_model = DummyAppAppContentPlugin


class DummyAppDetail(AllinkBaseDetailView):
    model = DummyApp
