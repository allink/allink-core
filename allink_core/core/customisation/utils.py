import os
from os.path import exists, join

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
