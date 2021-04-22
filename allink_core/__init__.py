import os

__version__ = '2.8.2'

# Cheeky setting that allows each template to be accessible by two paths.
# Eg: the template 'allink/templates/allink/base.html' can be accessed via both
# 'base.html' and 'allink/base.html'.  This allows allink's templates to be
# extended by templates with the same filename


ALLINK_CORE_MAIN_TEMPLATE_DIRS = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core/templates/allink_core'),
]

ALLINK_CORE_ALLINK_APPS = [
    'allink_core.apps.config',
    'allink_core.apps.locations',
    'allink_core.apps.news',
    'allink_core.apps.people',
    'allink_core.apps.partner',
]


def get_core_apps(overrides=None, installed=None):
    """
    Return a list of allink apps amended with any passed overrides
    """
    installed_apps = []
    if not installed:
        installed_apps = ALLINK_CORE_ALLINK_APPS
    else:
        for app in installed:
            if app in ALLINK_CORE_ALLINK_APPS:
                installed_apps.append(app)

    if not overrides:
        return installed_apps

    # Conservative import to ensure that this file can be loaded
    # without the presence Django.
    from django.utils import six
    if isinstance(overrides, six.string_types):
        raise ValueError(
            "get_core_apps expects a list or tuple of apps "
            "to override")

    def get_app_label(app_label, overrides):
        pattern = app_label.replace('allink_core.apps.', '')
        for override in overrides:
            if override.endswith(pattern):
                return override
        return app_label

    apps = []
    for app_label in installed_apps:
        apps.append(get_app_label(app_label, overrides))
    return apps
