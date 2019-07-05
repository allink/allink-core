import sys
import traceback
from importlib import import_module

from django.apps import apps
from django.apps.config import MODELS_MODULE_NAME
from django.conf import settings
from django.core.exceptions import AppRegistryNotReady

from allink_core.core.exceptions import (AppNotFoundError, ClassNotFoundError, ModuleNotFoundError)


def get_class(module_label, classname, module_prefix='allink_core.apps'):
    """
    Dynamically import a single class from the given module.
    This is a simple wrapper around `get_classes` for the case of loading a
    single class.
    Args:
        module_label (str): Module label comprising the app label and the
            module name, separated by a dot.  For example, 'news.forms'.
        classname (str): Name of the class to be imported.
    Returns:
        The requested class object or `None` if it can't be found
    """
    return get_classes(module_label, [classname], module_prefix)[0]


def get_classes(module_label, classnames, module_prefix='allink_core.apps'):
    """
    Dynamically import a list of classes from the given module.
    This works by looping over ``INSTALLED_APPS`` and looking for a match
    against the passed module label.  If the requested class can't be found in
    the matching module, then we attempt to import it from the corresponding
    core app.
    This is very similar to ``django.db.models.get_model`` function for
    dynamically loading models.  This function is more general though as it can
    load any class from the matching app, not just a model.
    Args:
        module_label (str): Module label comprising the app label and the
            module name, separated by a dot.  For example, 'news.forms'.
        classname (str): Name of the class to be imported.
    Returns:
        The requested class object or ``None`` if it can't be found
    Examples:
        Load a single class:
        >>> get_class('apps.news.forms', 'ProductForm')
        allink.apps.apps.news.forms.ProductForm
        Load a list of classes:
        >>> get_classes('apps.news.forms',
        ...             ['ProductForm', 'StockRecordForm'])
        [allink.apps.apps.news.forms.ProductForm,
         allink.apps.apps.news.forms.StockRecordForm]
    Raises:
        AppNotFoundError: If no app is found in ``INSTALLED_APPS`` that matches
            the passed module label.
        ImportError: If the attempted import of a class raises an
            ``ImportError``, it is re-raised
    """
    if '.' not in module_label:
        # Importing from top-level modules is not supported, e.g.
        # get_class('shipping', 'Scale'). That should be easy to fix,
        # but @maikhoepfel had a stab and could not get it working reliably.
        # Overridable classes in a __init__.py might not be a good idea anyway.
        raise ValueError(
            "Importing from top-level modules is not supported")

    # import from allink package (should succeed in most cases)
    # e.g. 'allink.apps.apps.news.forms'
    allink_module_label = "%s.%s" % (module_prefix, module_label)
    allink_module = _import_module(allink_module_label, classnames)

    # returns e.g. 'allink.apps.apps.news',
    # 'yourproject.apps.apps.news' or 'apps.news',
    # depending on what is set in INSTALLED_APPS
    installed_apps_entry, app_name = _find_installed_apps_entry(module_label)
    if installed_apps_entry.startswith('%s.' % module_prefix):
        # The entry is obviously an allink one, we don't import again
        local_module = None
    else:
        # Attempt to import the classes from the local module
        # e.g. 'yourproject.apps.news.forms'
        sub_module = module_label.replace(app_name, '', 1)
        local_module_label = installed_apps_entry + sub_module
        local_module = _import_module(local_module_label, classnames)

    allink_move_module = None

    if allink_module is allink_move_module is local_module is None:
        # This intentionally doesn't raise an ImportError, because ImportError
        # can get masked in complex circular import scenarios.
        raise ModuleNotFoundError(
            "The module with label '%s' could not be imported. This either"
            "means that it indeed does not exist, or you might have a problem"
            " with a circular import." % module_label
        )

    # return imported classes, giving preference to ones from the local package
    return _pluck_classes([local_module, allink_module, allink_move_module], classnames)


def _import_module(module_label, classnames):
    """
    Imports the module with the given name.
    Returns None if the module doesn't exist, but propagates any import errors.
    """
    try:
        return __import__(module_label, fromlist=classnames)
    except ImportError:
        # There are 2 reasons why there could be an ImportError:
        #
        #  1. Module does not exist. In that case, we ignore the import and
        #     return None
        #  2. Module exists but another ImportError occurred when trying to
        #     import the module. In that case, it is important to propagate the
        #     error.
        #
        # ImportError does not provide easy way to distinguish those two cases.
        # Fortunately, the traceback of the ImportError starts at __import__
        # statement. If the traceback has more than one frame, it means that
        # application was found and ImportError originates within the local app
        __, __, exc_traceback = sys.exc_info()
        frames = traceback.extract_tb(exc_traceback)
        if len(frames) > 1:
            raise


def _pluck_classes(modules, classnames):
    """
    Gets a list of class names and a list of modules to pick from.
    For each class name, will return the class from the first module that has a
    matching class.
    """
    klasses = []
    for classname in classnames:
        klass = None
        for module in modules:
            if hasattr(module, classname):
                klass = getattr(module, classname)
                break
        if not klass:
            packages = [m.__name__ for m in modules if m is not None]
            raise ClassNotFoundError("No class '%s' found in %s" % (
                classname, ", ".join(packages)))
        klasses.append(klass)
    return klasses


def _get_installed_apps_entry(app_name):
    """
    Given an app name (e.g. 'news'), walk through INSTALLED_APPS
    and return the first match, or None.
    This does depend on the order of INSTALLED_APPS and will break if
    e.g. 'apps.news' comes before 'news' in INSTALLED_APPS.
    """
    for installed_app in settings.INSTALLED_APPS:
        # match root-level apps ('news') or apps with same name at end
        # ('shop.news'), but don't match 'fancy_news'
        if installed_app == app_name or installed_app.endswith('.' + app_name):
            return installed_app
    return None


def _find_installed_apps_entry(module_label):
    """
    Given a module label, finds the best matching INSTALLED_APPS entry.
    This is made trickier by the fact that we don't know what part of the
    module_label is part of the INSTALLED_APPS entry. So we try all possible
    combinations, trying the longer versions first. E.g. for
    'apps.news.forms', 'apps.news' is attempted before
    'dashboard'
    """
    modules = module_label.split('.')
    # if module_label is 'apps.news.forms.widgets', combinations
    # will be ['apps.news.forms', 'apps.news', 'dashboard']
    combinations = [
        '.'.join(modules[:-count]) for count in range(1, len(modules))]
    for app_name in combinations:
        entry = _get_installed_apps_entry(app_name)
        if entry:
            return entry, app_name
    raise AppNotFoundError(
        "Couldn't find an app to import %s from" % module_label)


def get_model(app_label, model_name):
    """
    Fetches a Django model using the app registry.
    This doesn't require that an app with the given app label exists,
    which makes it safe to call when the registry is being populated.
    All other methods to access models might raise an exception about the
    registry not being ready yet.
    Raises LookupError if model isn't found.
    """
    try:
        return apps.get_model(app_label, model_name)
    except AppRegistryNotReady:
        if apps.apps_ready and not apps.models_ready:
            # If this function is called while `apps.populate()` is
            # loading models, ensure that the module that defines the
            # target model has been imported and try looking the model up
            # in the app registry. This effectively emulates
            # `from path.to.app.models import Model` where we use
            # `Model = get_model('app', 'Model')` instead.
            app_config = apps.get_app_config(app_label)
            # `app_config.import_models()` cannot be used here because it
            # would interfere with `apps.populate()`.
            import_module('%s.%s' % (app_config.name, MODELS_MODULE_NAME))
            # In order to account for case-insensitivity of model_name,
            # look up the model through a private API of the app registry.
            return apps.get_registered_model(app_label, model_name)
        else:
            # This must be a different case (e.g. the model really doesn't
            # exist). We just re-raise the exception.
            raise


def is_model_registered(app_label, model_name):
    """
    Checks whether a given model is registered. This is used to only
    register allink models if they aren't overridden by a forked app.
    """
    try:
        apps.get_registered_model(app_label, model_name)
    except LookupError:
        return False
    else:
        return True


def unregister_cms_menu(menu_cls):
    """
    Django CMS doesn't offer a function to unregister a cms menu
    Allows overriding cms menu in allink_apps
    """
    from menus.base import Menu
    from menus.menu_pool import menu_pool
    assert issubclass(menu_cls, Menu)
    if menu_cls.__name__ in menu_pool.menus:
        # Note: menu_cls should still be the menu CLASS at this point.
        del menu_pool.menus[menu_cls.__name__]


def unregister_cms_apps(app):
    """
    Django CMS doesn't offer a function to unregister a cms app
    Allows overriding cms apps in allink_apps
    """
    from cms.apphook_pool import apphook_pool

    if app.__name__ in apphook_pool.apps:
        del apphook_pool.apps[app.__name__]
