
from allink_core.allink_config.models import AllinkConfig


def allink_config(request):
    allink_config = AllinkConfig.get_solo()
    return {'allink_config': allink_config}
