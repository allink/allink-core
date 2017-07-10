# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from allink_core.core.cms_plugins import CMSAllinkBaseAppContentPlugin

from allink_core.core.loading import get_model


LocationsAppContentPlugin = get_model('locations', 'LocationsAppContentPlugin')


@plugin_pool.register_plugin
class CMSLocationsPlugin(CMSAllinkBaseAppContentPlugin):
    """
    model:
    - where to store plugin instances

    name:
    - name of the plugin
    """
    model = LocationsAppContentPlugin
    name = model.data_model.get_verbose_name_plural()

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(CMSLocationsPlugin, self).get_fieldsets(request, obj=None)
        fieldsets += (_('Map Options'), {
            'classes': (
                'collapse',
                'only_when_map',
            ),
            'fields': (
                'zoom_level',
            )
        }),
        return fieldsets
