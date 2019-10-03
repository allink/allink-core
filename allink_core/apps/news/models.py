# -*- coding: utf-8 -*allink_core/core/models/base_plugins.py-
from allink_core.apps.news.abstract_models import (
    BaseNews,
    BaseNewsTranslation,
    BaseNewsAppContentPlugin,
)
from allink_core.core.loading import get_model
from allink_core.core.loading import is_model_registered

__all__ = []

if not is_model_registered('news', 'News'):
    class News(BaseNews):
        pass

    __all__.append('News')

if not is_model_registered('news', 'NewsTranslation'):
    class NewsTranslation(BaseNewsTranslation):
        pass

    __all__.append('NewsTranslation')

if not is_model_registered('news', 'NewsAppContentPlugin'):
    class NewsAppContentPlugin(BaseNewsAppContentPlugin):
        data_model = get_model('news', 'News')

    __all__.append('NewsAppContentPlugin')
