# -*- coding: utf-8 -*-
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.core.cms_toolbars import AllinkBaseModifierMixin
from allink_core.core.loading import get_model

Config = get_model('config', 'Config')
Locations = get_model('locations', 'Locations')


class LocationsToolbar(AllinkBaseModifierMixin, CMSToolbar):
    model = Locations
    app_label = Locations._meta.app_label


toolbar_pool.register(LocationsToolbar)
