# -*- coding: utf-8 -*-
from cms.plugin_pool import plugin_pool
from allink_core.core.cms_plugins import CMSAllinkBaseAppContentPlugin

from allink_core.core.loading import get_model


LocationsAppContentPlugin = get_model('locations', 'LocationsAppContentPlugin')


@plugin_pool.register_plugin
class CMSLocationsAppContentPlugin(CMSAllinkBaseAppContentPlugin):
    """
    model:
    - where to store plugin instances

    name:
    - name of the plugin
    """
    model = LocationsAppContentPlugin
    name = model.data_model._meta.verbose_name_plural

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(CMSLocationsAppContentPlugin, self).get_fieldsets(request, obj=None)
        fieldsets += ('Map Options', {
            'classes': (
                'collapse',
                'only_when_map',
                'only_when_details_and_map',
            ),
            'fields': (
                'zoom_level',
            )
        }),
        return fieldsets
