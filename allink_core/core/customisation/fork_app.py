# -*- coding: utf-8 -*-
import logging
import os
import shutil
import textwrap
from os.path import exists, join
from .utils import create_local_app_folder, create_file, inherit_app_config
import allink_core

initial_snippet = '# -*- coding: utf-8 -*-\n'

help_admin = '''
"""
use core:
from allink_core.apps.{app_package}.admin import *  # noqa

override example:
from allink_core.apps.{app_package}.admin import *  # noqa

admin.site.unregister({model_name})

@admin.register({model_name})
class {model_name}Admin({model_name}Admin):
    pass
"""\n'''

help_apps = '''
"""
use core:
from allink_core.apps.{app_package}.cms_apps import *  # noqa

override example:
from allink_core.core.loading import unregister_cms_apps
from allink_core.apps.{app_package}.cms_apps import *  # noqa

unregister_cms_apps({model_name}Apphook)

class {model_name}Apphook({model_name}Apphook):
    def get_urls(self, page=None, language=None, **kwargs):
        urls = super({model_name}Apphook, self).get_urls(page=None, language=None, **kwargs)
        return urls + ['allink_apps.{app_package}.urls']

apphook_pool.register({model_name}Apphook)
"""\n'''

help_menus = '''
"""
use core:
from allink_core.apps.{app_package}.cms_menus import *  # noqa

override example:
from allink_core.core.loading import unregister_cms_menu
from allink_core.apps.{app_package}.cms_menus import *  # noqa

unregister_cms_menu({model_name}Menu)

class {model_name}Menu({model_name}Menu):
   pass

menu_pool.register_menu(get_class('{app_package}.cms_menus', '{model_name}Menu'))
"""\n'''


help_cms_plugins = '''
"""
use core:
from allink_core.apps.{app_package}.cms_plugins import *  # noqa

override example:
from allink_core.apps.{app_package}.cms_plugins import *  # noqa

plugin_pool.unregister_plugin(CMS{model_name}AppContentPlugin)

@plugin_pool.register_plugin
class CMS{model_name}AppContentPlugin(CMS{model_name}AppContentPlugin):
    pass
"""\n'''

help_toolbars = '''
"""
use core:
from allink_core.apps.{app_package}.cms_toolbars import *  # noqa

override example:
from allink_core.allink_base.utils.loading import get_model
from allink_core.apps.{app_package}.cms_toolbars import *  # noqa

from allink_core.core.cms_toolbars import AllinkBaseModifierMixin
Config = get_model('config', 'Config')

toolbar_pool.unregister({model_name}Toolbar)


class {model_name}Toolbar({model_name}Toolbar):
    pass

if getattr(Config.get_solo(), '{app_package}_toolbar_enabled', True):
    toolbar_pool.register({model_name}Toolbar)
    pass
"""\n'''

help_models = '''
"""
use core:
from allink_core.apps.{app_package}.models import *  # noqa

override example:
you don't have to override every model

from django.db import models
from allink_core.apps.{app_package}.abstract_models import Base{model_name}, Base{model_name}Translation, Base{model_name}AppContentPlugin
from allink_core.core.loading import get_model


class {model_name}(Base{model_name}):
    pass


class {model_name}Translation(Base{model_name}Translation):
    pass


class {model_name}AppContentPlugin(Base{model_name}AppContentPlugin):
    data_model = get_model('{app_package}', '{model_name}')
    pass

from allink_core.apps.{app_package}.models import *  # noqa
"""\n'''

help_managers = '''
"""
use core:
from allink_core.apps.{app_package}.managers import *  # noqa

override example:
# -*- coding: utf-8 -*-
from datetime import datetime
from django.db.models import Q
from allink_core.apps.{app_package}.managers import Allink{model_name}QuerySet


class Allink{model_name}QuerySet(Allink{model_name}QuerySet):
    pass


Allink{model_name}Manager = Allink{model_name}QuerySet.as_manager
"""\n'''

help_sitemaps = '''# -*- coding: utf-8 -*-
"""
use core:
no 'sitemaps.py' file needed

override example:
from allink_core.apps.{app_package}.sitemaps import {model_name}Sitemap as Core{model_name}Sitemap

class {model_name}Sitemap(Core{model_name}Sitemap):
    pass
"""\n'''

snippet_urls = '''# -*- coding: utf-8 -*-
"""
use core:
no 'urls.py' file needed

override example:
!important!
make sure you also add the new urls to the cms_apps.py so djangocms knows about them!
ovverride the apphook, see example in cms_apps.py


from django.urls import path
from allink_apps.{app_package}.views import new_view


urlpatterns = [
    path('new-view/<int:id>/', new_view, name='new-view'),
]
"""\n'''

snippet_views = '''# -*- coding: utf-8 -*-
"""
use core:
no 'views.py' file needed

override example:
from allink_core.apps.{app_package}.views import {model_name}Detail as Core{model_name}Detail

class {model_name}Detail(Base{model_name}Detail):
    ...
    def render_to_response(self, context, **response_kwargs):
        if self.request.GET.get('softpage', None):
            context.update({'base_template': 'app_content/ajax_base.html'})
        context.update({'hello': 'hello view is correctly overridden!!'})
        return render_to_response(self.get_template_names(), context, context_instance=RequestContext(self.request))

# TO ADD NEW VIEW:
import datetime
from django.http import HttpResponse
from allink_core.core.loading import get_model
from allink_core.apps.{app_package}.pdf import Pdf{model_name}

{model_name} = get_model('{app_package}', '{model_name}')

def export_pdf(request, id):
    date = (datetime.date.today().strftime('%d-%m-%Y'))

    item = {model_name}.objects.get(id=id)

    pdf = Pdf{model_name}(item, request)
    output = pdf.build()
    filename = '%s_%s.pdf' % (item.title, date)

    response = HttpResponse(output.getvalue(), content_type="application/pdf")
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
"""\n'''


def fork_app(label, folder_path, logger=None, help=False):  # noqa
    """
    Create a custom version of one of allink's apps
    (help: Including helpful comments to get you started)

    """

    # Create minimum app files
    app_package = label
    model_name = label.title().replace('_', '')

    # Create all snippets
    snippet_admin = initial_snippet
    snippet_cms_apps = initial_snippet
    snippet_menus = initial_snippet
    snippet_cms_plugins = initial_snippet
    snippet_toolbars = initial_snippet
    snippet_managers = initial_snippet
    snippet_models = initial_snippet
    snippet_sitemaps = initial_snippet

    if help:
        snippet_admin += help_admin.format(app_package=label, model_name=model_name)
        snippet_cms_apps += help_apps.format(app_package=label, model_name=model_name)
        snippet_menus += help_menus.format(app_package=label, model_name=model_name)
        snippet_cms_plugins += help_cms_plugins.format(app_package=label, model_name=model_name)
        snippet_toolbars += help_toolbars.format(app_package=label, model_name=model_name)
        snippet_managers += help_managers.format(app_package=label, model_name=model_name)
        snippet_models += help_models.format(app_package=label, model_name=model_name)
        snippet_sitemaps += help_sitemaps.format(app_package=label, model_name=model_name)

    snippet_admin += "from allink_core.apps.{}.admin import *  # noqa\n".format(label)
    snippet_cms_apps += "from allink_core.apps.{}.cms_apps import *  # noqa\n".format(label)
    snippet_menus += "from allink_core.apps.{}.cms_menus import *  # noqa\n".format(label)
    snippet_cms_plugins += "from allink_core.apps.{}.cms_plugins import *  # noqa\n".format(label)
    snippet_toolbars += "from allink_core.apps.{}.cms_toolbars import *  # noqa\n".format(label)
    snippet_managers += "from allink_core.apps.{}.managers import *  # noqa\n".format(label)
    snippet_models += "from allink_core.apps.{}.models import *  # noqa\n".format(label)

    if logger is None:
        logger = logging.getLogger(__name__)

    # Check label is valid
    valid_labels = [x.replace('allink_core.apps.', '')
                    for x in allink_core.ALLINK_CORE_ALLINK_APPS if x.startswith('allink_core')]
    if label not in valid_labels:
        raise ValueError("There is no allink_core app that matches '%s'" % label)

    # Check folder_path is current catalog
    if folder_path == '.':
        folder_path = ''

    # Create folder
    label_folder = label.replace('.', '/')
    local_app_path = join(folder_path, label_folder)
    logger.info("Creating package %s" % local_app_path)
    create_local_app_folder(local_app_path)

    # Create minimum app files
    app_package = local_app_path.replace('/', '.')

    allink_core_app_path = join(allink_core.__path__[0], 'apps', label_folder)
    if exists(os.path.join(allink_core_app_path, 'admin.py')):
        logger.info("Creating admin.py")
        create_file(join(local_app_path, 'admin.py'), snippet_admin)

    logger.info("Creating app config")
    inherit_app_config(local_app_path, app_package, label)

    # Only create models.py and migrations if it exists in the allink_core app
    allink_core_models_path = join(allink_core_app_path, 'models.py')
    if exists(allink_core_models_path):
        logger.info("Creating models.py")
        create_file(
            join(local_app_path, 'models.py'), snippet_models)

        migrations_path = 'migrations'
        source = join(allink_core_app_path, migrations_path)
        if exists(source):
            logger.info("Creating %s folder", migrations_path)
            destination = join(local_app_path, migrations_path)
            shutil.copytree(source, destination)

    # cms_apps.py
    if exists(os.path.join(allink_core_app_path, 'cms_apps.py')):
        logger.info("Creating cms_apps.py")
        create_file(join(local_app_path, 'cms_apps.py'), snippet_cms_apps)

    # cms_menus.py
    if exists(os.path.join(allink_core_app_path, 'cms_menus.py')):
        logger.info("Creating cms_menus.py")
        create_file(join(local_app_path, 'cms_menus.py'), snippet_menus)

    # cms_plugins.py
    if exists(os.path.join(allink_core_app_path, 'cms_plugins.py')):
        logger.info("Creating admin.py")
        create_file(join(local_app_path, 'cms_plugins.py'), snippet_cms_plugins)

    # cms_toolbars.py
    if exists(os.path.join(allink_core_app_path, 'cms_toolbars.py')):
        logger.info("Creating cms_toolbars.py")
        create_file(join(local_app_path, 'cms_toolbars.py'), snippet_toolbars)

    # only for help
    if help:
        if exists(os.path.join(allink_core_app_path, 'sitemaps.py')):
            logger.info("Creating sitemaps.py")
            create_file(join(local_app_path, 'sitemaps.py'), snippet_sitemaps)

        if exists(os.path.join(allink_core_app_path, 'managers.py')):
            logger.info("Creating managers.py")
            create_file(join(local_app_path, 'managers.py'), snippet_managers)

        if exists(os.path.join(allink_core_app_path, 'urls.py')):
            logger.info("Creating urls.py")
            create_file(join(local_app_path, 'urls.py'), snippet_urls)

        if exists(os.path.join(allink_core_app_path, 'views.py')):
            logger.info("Creating views.py")
            create_file(join(local_app_path, 'views.py'), snippet_views)

    # Final step needs to be done by hand
    msg = (
        "The final step is to uncomment '%s' in OVERRIDDEN_ALLINK_CORE_APPS "
        "(replacing the equivalent allink_core app). e.g.:"
    ) % app_package
    snippet = (
        "  # settings.py\n"
        "  ...\n"
        "  OVERRIDDEN_ALLINK_CORE_APPS = [\n"
        "      ['%s'],"
        "      ...\n"
        "  ]\n"
    ) % app_package
    record = "\n%s\n\n%s" % (
        "\n".join(textwrap.wrap(msg)), snippet)
    logger.info(record)