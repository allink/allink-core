import os
import shutil
import importlib
from distutils.dir_util import copy_tree
from distutils.errors import DistutilsFileError
from allink_core import ALLINK_CORE_ALLINK_APPS

__all__ = [
    'get_path',
    'copy_dir',
    'replace_strings',
    'rename',
    'fork_allink_app',
    'create_new_app',
]


def get_path(module_str):
    """
    :param module_str
    the module string e.g 'allink_core.core.customisation.dummy_app'
    :return
    the path to the directory e.g '/usr/local/lib/python3.6/site-packages/allink-core/core/customisation/dummy_app'
    """
    module = importlib.import_module(module_str)
    return os.path.dirname(module.__file__)


def copy_dir(dummy_app, app_path):
    """
    copies a directory to another directory

    :param dummy_app:
    path to directory e.g 'allink_core/core/customisation/dummy_app'
    :param app_path:
    path where the new app should created in
    :return
    destination dir
    """
    if os.path.isdir(app_path):
        raise OSError("Can't create destination directory. '{}' directory already exists!".format(app_path))
    try:
        dst = copy_tree(dummy_app, app_path)
    except (OSError, DistutilsFileError) as e:
        raise e

    return dst


def replace_strings(file_path, replace):
    """
    replace strings in a file

    :param file_path:
    path to file
    :param replace:
    dict of strings to replace. e.g:
    replace = {
        'dummy_app': 'new_app',
        'DummyApp': 'NewApp',
        'dummy-app': 'new-app',
    }
    """
    with open(file_path, 'r') as f:
        s = f.read()
        for item in replace.items():
            s = s.replace(item[0], item[1])

    with open(file_path, 'w') as f:
        f.write(s)


def rename(path, replace):
    """
    renames directory or file
    :param path:
    path to file or dir
    :param replace:
    dict of strings to replace. e.g:
    replace = {
        'dummy_app': 'new_app',
        'dummyapp': 'newapp',
        'dummyapp': model_name.lower(),  # lower model name
    }
    :return:
    new dir file path
    """
    basename = os.path.basename(path)
    if any(sub in basename for sub in replace.keys()):
        for item in filter(lambda i: i[0] in basename, replace.items()):
            new_base = basename.replace(item[0], item[1])
            new_path = os.path.join(os.path.dirname(path), new_base)
            os.replace(path, new_path)
            path = new_path


def rename_and_replace(path, replace):
    """
    renames and replaces strings in:
     - filenames
     - directories
     - inside files

    :param path:
    the path in which all files and dirs should be renamed and replaced
    :param replace:
    a dict containing all the  strings which should be replaced
    """
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if not dir == '__pycache__':
                # rename directories
                dir_path = os.path.join(root, dir)
                rename(path=dir_path, replace=replace)

    # file renaming needs to be done in a second iteration as the directory names have changed
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith('.pyc'):
                # rename file names
                file_path = os.path.join(root, file)
                # rename dummy classes and import statements
                replace_strings(file_path=file_path, replace=replace)
                # rename file and dir names
                rename(path=file_path, replace=replace)


def create_new_app(dummy_app, app_path, app_label, model_name):
    """
    copies a dummy_app directory renames and replaces dummy naming

    :param dummy_app:
    path to dummy_app e.g 'allink_core.core.customisation.dummy_app'
    :param app_path:
    path where the new app should created e.g 'apps'
    :param app_label:
    new app directory name e.g 'new_app'
    :param model_name:
    new model name name e.g 'NewApp'
    """
    dummy_app_path = get_path(dummy_app)
    new_app_path = os.path.join(app_path, app_label)

    # copy directory
    copy_dir(dummy_app_path, new_app_path)

    replace = {
        'dummy_app': app_label,  # app label
        'DummyApp': model_name,  # model name
        'dummy-app': app_label.replace('_', '-'),  # css class
        'dummyapp': model_name.lower(),  # lower model name
    }
    rename_and_replace(new_app_path, replace)


def fork_allink_app(dummy_app, app_path, app_label):
    """
    forks an app in alink_core.apps
     - renames and replaces dummy naming
     - copies all existing migrations

    :param dummy_app:
    path to dummy_app e.g 'allink_core.core.customisation.dummy_fork_app'
    :param app_path:
    path where the new app should created e.g 'apps'
    :param app_label:
    app label e.g 'news' needs to be in ALLINK_CORE_ALLINK_APPS
    """
    dummy_app_path = get_path(dummy_app)
    allink_core_app_path = os.path.join(get_path('allink_core.apps'), app_label)
    new_app_path = os.path.join(app_path, app_label)
    model_name = app_label.capitalize()

    if not any(app_label in app.split('.')[-1] for app in ALLINK_CORE_ALLINK_APPS):
        raise ValueError("There is no allink_core app with the app_label '{}'".format(app_label))

    # copy directory
    copy_dir(dummy_app_path, new_app_path)

    replace = {
        'dummy_app': app_label,  # app label
        'DummyApp': model_name,  # model name
        'dummy-app': app_label.replace('_', '-'),  # css class
        'dummyapp': model_name.lower(),  # lower model name
    }
    rename_and_replace(new_app_path, replace)

    # copy migrations from allink_core app_path to the new app_path
    shutil.copytree(
        os.path.join(allink_core_app_path, 'migrations'),
        os.path.join(new_app_path, 'migrations')
    )
