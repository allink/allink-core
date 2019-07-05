# -*- coding: utf-8 -*-
from allink_core.apps.locations.abstract_models import BaseLocations, BaseLocationsTranslation, \
    BaseLocationsAppContentPlugin
from allink_core.core.loading import get_model
from allink_core.core.loading import is_model_registered

__all__ = []


if not is_model_registered('locations', 'Locations'):
    class Locations(BaseLocations):
        pass

    __all__.append('Locations')


if not is_model_registered('locations', 'LocationsTranslation'):
    class LocationsTranslation(BaseLocationsTranslation):
        pass

    __all__.append('LocationsTranslation')


if not is_model_registered('locations', 'LocationsAppContentPlugin'):
    class LocationsAppContentPlugin(BaseLocationsAppContentPlugin):
        data_model = get_model('locations', 'Locations')

    __all__.append('LocationsAppContentPlugin')
