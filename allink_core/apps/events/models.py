# -*- coding: utf-8 -*-
from allink_core.apps.events.abstract_models import (
    BaseEvents,
    BaseEventsTranslation,
    BaseEventsAppContentPlugin,
    BaseEventsRegistration
)
from allink_core.core.loading import get_model
from allink_core.core.loading import is_model_registered

__all__ = []


# Events
if not is_model_registered('events', 'Events'):
    class Events(BaseEvents):
        pass

    __all__.append('Events')


if not is_model_registered('events', 'EventsTranslation'):
    class EventsTranslation(BaseEventsTranslation):
        pass

    __all__.append('EventsTranslation')


if not is_model_registered('events', 'EventsAppContentPlugin'):
    class EventsAppContentPlugin(BaseEventsAppContentPlugin):
        data_model = get_model('events', 'Events')

    __all__.append('EventsAppContentPlugin')


if not is_model_registered('events', 'EventsRegistration'):
    class EventsRegistration(BaseEventsRegistration):
        pass

    __all__.append('EventsRegistration')
