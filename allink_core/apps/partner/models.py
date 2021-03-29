# -*- coding: utf-8 -*allink_core/core/models/base_plugins.py-
from allink_core.apps.partner.abstract_models import (
    BasePartner,
    BasePartnerTranslation,
    BasePartnerAppContentPlugin,
)
from allink_core.core.loading import get_model
from allink_core.core.loading import is_model_registered

__all__ = []

if not is_model_registered('partner', 'Partner'):
    class Partner(BasePartner):
        pass

    __all__.append('Partner')

if not is_model_registered('partner', 'PartnerTranslation'):
    class PartnerTranslation(BasePartnerTranslation):
        pass

    __all__.append('PartnerTranslation')

if not is_model_registered('partner', 'PartnerAppContentPlugin'):
    class PartnerAppContentPlugin(BasePartnerAppContentPlugin):
        data_model = get_model('partner', 'Partner')

    __all__.append('PartnerAppContentPlugin')
