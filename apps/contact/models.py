# -*- coding: utf-8 -*-
from allink_core.apps.contact.abstract_models import BaseContactRequest, BaseContactRequestPlugin
from allink_core.core.loading import is_model_registered
from allink_core.core.loading import get_class

__all__ = []


if not is_model_registered('contact', 'ContactRequest'):
    class ContactRequest(BaseContactRequest):
        pass

    __all__.append('ContactRequest')


if not is_model_registered('contact', 'ContactRequestPlugin'):
    class ContactRequestPlugin(BaseContactRequestPlugin):
        form_class = get_class('contact.forms', 'ContactRequestForm')

    __all__.append('ContactRequestPlugin')
