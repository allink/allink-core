# -*- coding: utf-8 -*-

from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView
from allink_core.core.loading import get_model


People = get_model('people', 'People')
PeopleAppContentPlugin = get_model('people', 'PeopleAppContentPlugin')


class PeoplePluginLoadMore(AllinkBasePluginLoadMoreView):
    model = People
    plugin_model = PeopleAppContentPlugin


class PeopleDetail(AllinkBaseDetailView):
    model = People
