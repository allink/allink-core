import os
from os.path import exists, join
from distutils.dir_util import copy_tree

__all__ = [
    'create_local_app_folder',
    'subfolders',
    'inherit_app_config',
    'create_file',
]


def create_local_app_folder(local_app_path):
    if exists(local_app_path):
        raise ValueError("There is already a '%s' folder! Aborting!" % local_app_path)

    for folder in subfolders(local_app_path):
        if not exists(folder):
            os.mkdir(folder)
            init_path = join(folder, '__init__.py')
            if not exists(init_path):
                create_file(init_path)


def subfolders(path):
    """
    Decompose a path string into a list of subfolders

    Eg Convert 'apps/dashboard/ranges' into
       ['apps', 'apps/dashboard', 'apps/dashboard/ranges']
    """
    folders = []
    while path not in ('/', ''):
        folders.append(path)
        path = os.path.dirname(path)
    folders.reverse()
    return folders


def inherit_app_config(local_app_path, app_package, app_label):
    config_name = app_label.title() + 'Config'
    create_file(
        join(local_app_path, '__init__.py'),
        "default_app_config = '{app_package}.config.{config_name}'\n".format(
            app_package=app_package, config_name=config_name))
    create_file(
        join(local_app_path, 'config.py'),
        "from allink_core.apps.{app_label} import config\n\n\n"
        "class {config_name}(config.{config_name}):\n"
        "    name = '{app_package}'\n".format(
            app_package=app_package,
            app_label=app_label,
            config_name=config_name))


def create_file(filepath, content=''):
    with open(filepath, 'w') as f:
        f.write(content)


def copy_dummy_dir(dummy_path, app_path):
    """
    copies a dummy directory to another directory
    :param dummy_path:
    path to dummy_app e.g 'allink_core/core/customisation/dummy_app'
    :param app_path:
    path where the new app should created in
    :return
    destination dir
    """
    if os.path.isdir(app_path):
        raise OSError("Can't create destination directory. '{}' directory already exists!".format(app_path))
    try:
        dst = copy_tree(dummy_path, app_path)
    except OSError as e:
        raise e

    return dst


def rename_dummy_classes(file_path, replace):
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
    with open(file_path, "rt") as f:
        s = f.read()
        for item in replace.items():
            s = s.replace(item[0], item[1])

    with open(file_path, "w") as f:
        f.write(s)


def rename_dummy_file_name(file_path):
    """
    replaced file names of a given file
    :param file_path:
    path to file
    """
    pass


def create_new_app(dummy_path, app_path, app_label, model_name):
    """
    :param dummy_path:
    path to dummy_app e.g 'allink_core/core/customisation/dummy_app'
    :param app_path:
    path where the new app should created e.g 'apps'
    :param app_name:
    new app directory name e.g 'new_app'
    :return:
    new directory
    """

    replace = {
        'dummy_app': app_label,  # app label
        'DummyApp': model_name,  # model name
        'dummy-app': app_label.replace('_', '-'),  # css class
    }

    new_app_path = os.path.join(app_path, app_label)

    # copy directory
    new_dir = copy_dummy_dir(dummy_path, new_app_path)

    # remove 'README.md'
    readme = os.path.join(new_app_path, 'README.md')
    os.remove(readme)

    for root, dirs, files in os.walk(new_dir):
        # rename dummy classes and import statements
        rename_dummy_classes(file_path=files, replace=replace)
        # rename file names
        rename_dummy_file_name(file_path=files)

    return new_dir
