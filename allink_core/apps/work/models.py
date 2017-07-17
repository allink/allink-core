# -*- coding: utf-8 -*-
from allink_core.apps.work.abstract_models import BaseWork, BaseWorkTranslation, BaseWorkAppContentPlugin, BaseWorkSearchPlugin
from allink_core.core.loading import get_model
from allink_core.core.loading import is_model_registered

__all__ = []


if not is_model_registered('work', 'Work'):
    class Work(BaseWork):
        pass

    __all__.append('Work')


if not is_model_registered('work', 'WorkTranslation'):
    class WorkTranslation(BaseWorkTranslation):
        pass

    __all__.append('WorkTranslation')


if not is_model_registered('work', 'WorkAppContentPlugin'):
    class WorkAppContentPlugin(BaseWorkAppContentPlugin):
        data_model = get_model('work', 'Work')

    __all__.append('WorkAppContentPlugin')


if not is_model_registered('work', 'WorkSearchPlugin'):
    class WorkSearchPlugin(BaseWorkSearchPlugin):
        data_model = get_model('work', 'Work')

    __all__.append('WorkSearchPlugin')
