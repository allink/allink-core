# -*- coding: utf-8 -*-
from allink_core.apps.config.abstract_models import BaseConfig, BaseConfigTranslation
from allink_core.core.loading import is_model_registered

__all__ = []


if not is_model_registered('config', 'Config'):
    class Config(BaseConfig):
        pass

    __all__.append('Config')


if not is_model_registered('config', 'ConfigTranslation'):
    class ConfigTranslation(BaseConfigTranslation):
        pass

    __all__.append('ConfigTranslation')
