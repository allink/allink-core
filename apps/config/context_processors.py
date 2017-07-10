# -*- coding: utf-8 -*-
from allink_core.core.loading import get_model

Config = get_model('config', 'Config')


def config(request):
    """
    if you want to override this processor, make sure you change settings.py accordingly
    context_processors.extend([
        ...
        'allink_apps.config.context_processors',
    ])
    """
    return {'config': Config.get_solo()}
