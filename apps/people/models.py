# -*- coding: utf-8 -*-
from allink_core.apps.people.abstract_models import BasePeople, BasePeopleTranslation, BasePeopleAppContentPlugin
from allink_core.core.loading import get_model
from allink_core.core.loading import is_model_registered

__all__ = []


if not is_model_registered('people', 'People'):
    class People(BasePeople):
        pass

    __all__.append('People')


if not is_model_registered('people', 'PeopleTranslation'):
    class PeopleTranslation(BasePeopleTranslation):
        pass

    __all__.append('PeopleTranslation')


if not is_model_registered('people', 'PeopleAppContentPlugin'):
    class PeopleAppContentPlugin(BasePeopleAppContentPlugin):
        data_model = get_model('people', 'People')

    __all__.append('PeopleAppContentPlugin')
