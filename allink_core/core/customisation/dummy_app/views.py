# -*- coding: utf-8 -*-
from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView
from .models import TestApp, TestAppAppContentPlugin


class TestAppPluginLoadMore(AllinkBasePluginLoadMoreView):
    model = TestApp
    plugin_model = TestAppAppContentPlugin


class TestAppDetail(AllinkBaseDetailView):
    model = TestApp
