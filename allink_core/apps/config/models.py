# -*- coding: utf-8 -*-

from cms.extensions.extension_pool import extension_pool
from allink_core.core.loading import is_model_registered

from allink_core.apps.config.abstract_models import (
    BaseConfig, BaseConfigTranslation, BaseAllinkPageExtension,
    BaseAllinkTitleExtension,
)

__all__ = []

if not is_model_registered('config', 'Config'):
    class Config(BaseConfig):
        pass

    __all__.append('Config')

if not is_model_registered('config', 'ConfigTranslation'):
    class ConfigTranslation(BaseConfigTranslation):
        pass

    __all__.append('ConfigTranslation')

if not is_model_registered('config', 'AllinkPageExtension'):
    class AllinkPageExtension(BaseAllinkPageExtension):
        pass

    __all__.append('AllinkPageExtension')

    extension_pool.register(AllinkPageExtension)

if not is_model_registered('config', 'AllinkTitleExtension'):
    class AllinkTitleExtension(BaseAllinkTitleExtension):
        pass

    __all__.append('AllinkTitleExtension')
    extension_pool.register(AllinkTitleExtension)
