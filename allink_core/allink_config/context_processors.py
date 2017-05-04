from allink_core.allink_config.models import AllinkConfig


def allink_config(request):
    return {'allink_config': AllinkConfig.get_solo()}
