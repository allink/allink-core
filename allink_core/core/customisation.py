# -*- coding: utf-8 -*-

import logging
import os
import shutil
import textwrap
from os.path import exists, join

import allink_core


def create_local_app_folder(local_app_path):
    if exists(local_app_path):
        raise ValueError(
            "There is already a '%s' folder! Aborting!" % local_app_path)
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


initial_snippet = '# -*- coding: utf-8 -*-\n'

help_admin ='''
"""
use core:
from allink_core.apps.work.admin import *  # noqa

override example:
from allink_core.apps.work.admin import *  # noqa

admin.site.unregister(Work)

@admin.register(Work)
class WorkAdmin(WorkAdmin):
    pass
"""\n'''

help_apps ='''
"""
use core:
from allink_core.apps.work.cms_apps import *  # noqa

override example:
from allink_core.core.loading import unregister_cms_apps
from allink_core.apps.work.cms_apps import *  # noqa

unregister_cms_apps(WorkApphook)

class WorkApphook(WorkApphook):
    def get_urls(self, page=None, language=None, **kwargs):
        urls = super(WorkApphook, self).get_urls(page=None, language=None, **kwargs)
        return urls + ['allink_apps.work.urls']

apphook_pool.register(WorkApphook)
"""\n'''

help_menus ='''
"""
use core:
from allink_core.apps.work.cms_menus import *  # noqa

override example:
from allink_core.core.loading import unregister_cms_menu
from allink_core.apps.work.cms_menus import *  # noqa

unregister_cms_menu(WorkMenu)

class WorkMenu(WorkMenu):
   pass

menu_pool.register_menu(get_class('work.cms_menus', 'WorkMenu'))
"""\n'''


help_cms_plugins ='''
"""
use core:
from allink_core.apps.work.cms_plugins import *  # noqa

override example:
from allink_core.apps.work.cms_plugins import *  # noqa

plugin_pool.unregister_plugin(CMSWorkAppContentPlugin)

@plugin_pool.register_plugin
class CMSWorkAppContentPlugin(CMSWorkAppContentPlugin):
    pass
"""\n'''

help_toolbars ='''
"""
use core:
from allink_core.apps.work.cms_toolbars import *  # noqa

override example:
from allink_core.allink_base.utils.loading import get_model
from allink_core.apps.work.cms_toolbars import *  # noqa

from allink_core.core.cms_toolbars import AllinkBaseModifierMixin
Config = get_model('config', 'Config')

toolbar_pool.unregister(WorkToolbar)


class WorkToolbar(WorkToolbar):
    pass

if getattr(Config.get_solo(), 'work_toolbar_enabled', True):
    toolbar_pool.register(WorkToolbar)
    pass
"""\n'''

help_models ='''
"""
use core:
from allink_core.apps.work.models import *  # noqa

override example:
you don't have to override every model

from django.db import models
from allink_core.apps.work.abstract_models import BaseWork, BaseWorkTranslation, BaseWorkAppContentPlugin
from allink_core.core.loading import get_model


class Work(BaseWork):
    pass


class WorkTranslation(BaseWorkTranslation):
    pass


class WorkAppContentPlugin(BaseWorkAppContentPlugin):
    data_model = get_model('work', 'Work')
    pass

from allink_core.apps.work.models import *  # noqa
"""\n'''

snippet_sitemaps ='''# -*- coding: utf-8 -*-
"""
use core:
no 'sitemaps.py' file needed

override example:
from allink_core.apps.work.sitemaps import WorkSitemap as CoreWorkSitemap

class WorkSitemap(BaseWorkSitemap):
    pass
"""\n'''

snippet_urls ='''# -*- coding: utf-8 -*-
"""
use core:
no 'urls.py' file needed

override example:
!important!
make sure you also add the new urls to the cms_apps.py so djangocms knows about them!
ovverride the apphook, see example in cms_apps.py


from django.conf.urls import url
from allink_apps.work.views import new_view


urlpatterns = [
    url(r'^new-view/(?P<id>[0-9]+)/$', new_view, name='new-view'),
]
"""\n'''

snippet_views ='''# -*- coding: utf-8 -*-
"""
use core:
no 'views.py' file needed

override example:
from allink_core.apps.work.views import WorkDetail as CoreWorkDetail

class WorkDetail(BaseWorkDetail):
    ...
    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            context.update({'base_template': 'app_content/ajax_base.html'})
        context.update({'hello': 'hello view is correctly overridden!!'})
        return render_to_response(self.get_template_names(), context, context_instance=RequestContext(self.request))

# TO ADD NEW VIEW:
import datetime
from django.http import HttpResponse
from allink_core.core.loading import get_model
from allink_core.apps.work.pdf import PdfWork

Work = get_model('work', 'Work')

def export_pdf(request, id):
    date = (datetime.date.today().strftime('%d-%m-%Y'))

    item = Work.objects.get(id=id)

    pdf = PdfWork(item, request)
    output = pdf.build()
    filename = '%s_%s.pdf' % (item.title, date)

    response = HttpResponse(output.getvalue(), content_type="application/pdf")
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
"""\n'''


def fork_app(label, folder_path, logger=None, help=False):
    """
    Create a custom version of one of allink's apps
    (help: Including helpful comments to get you started)

    """

    snippet_admin = initial_snippet
    snippet_cms_apps = initial_snippet
    snippet_menus = initial_snippet
    snippet_cms_plugins = initial_snippet
    snippet_toolbars = initial_snippet
    snippet_models = initial_snippet

    if help:
        snippet_admin += help_admin
        snippet_cms_apps += help_apps
        snippet_menus += help_menus
        snippet_cms_plugins += help_cms_plugins
        snippet_toolbars += help_toolbars
        snippet_models += help_models

    snippet_admin += "from allink_core.apps.{}.admin import *  # noqa\n".format(label)
    snippet_cms_apps += "from allink_core.apps.{}.cms_apps import *  # noqa\n".format(label)
    snippet_menus += "from allink_core.apps.{}.cms_menus import *  # noqa\n".format(label)
    snippet_cms_plugins += "from allink_core.apps.{}.cms_plugins import *  # noqa\n".format(label)
    snippet_toolbars += "from allink_core.apps.{}.cms_toolbars import *  # noqa\n".format(label)
    snippet_models += "from allink_core.apps.{}.models import *  # noqa\n".format(label)

    if logger is None:
        logger = logging.getLogger(__name__)

    # Check label is valid
    valid_labels = [x.replace('allink_core.apps.', '') for x in allink_core.ALLINK_CORE_ALLINK_APPS if x.startswith('allink_core')]
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


new_admin = '''# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from cms.admin.placeholderadmin import PlaceholderAdminMixin
from allink_core.core.admin import AllinkBaseAdminSortable

from {app_package}.models import {model_name}


@admin.register({model_name})
class {model_name}Admin(PlaceholderAdminMixin, AllinkBaseAdminSortable):
    list_filter = ('status', 'categories',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            (None, {{
                'fields': (
                    'status',
                    'title',
                    'slug',
                    'lead',
                    'preview_image',
                ),
            }}),
        )

        fieldsets += self.get_base_fieldsets()

        return fieldsets

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'lead':
            kwargs['widget'] = forms.Textarea
        return super({model_name}Admin, self).formfield_for_dbfield(db_field, **kwargs)

'''

new_cms_apps = '''# -*- coding: utf-8 -*-
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class {model_name}Apphook(CMSApp):
    name = _("{model_name} Apphook")
    app_name = '{label}'

    def get_urls(self, page=None, language=None, **kwargs):
        return ['{app_package}.urls']


apphook_pool.register({model_name}Apphook)

'''

new_cms_menu = '''# -*- coding: utf-8 -*-
from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _
from cms.menu_bases import CMSAttachMenu

from {app_package}.models import {model_name}


class {model_name}Menu(CMSAttachMenu):

    name = _("{model_name} menu")

    def get_nodes(self, request):

        nodes = []
        for entry in {model_name}.objects.active():
            node = NavigationNode(
                entry.title,
                entry.get_absolute_url(),
                entry.sort_order,
                attr={{
                    'description': entry.lead
                }})
            nodes.append(node)

        return nodes


menu_pool.register_menu('{app_package}.cms_menus', '{model_name}Menu')

'''

new_cms_plugins = '''# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from allink_core.core.cms_plugins import CMSAllinkBaseAppContentPlugin

from {app_package}.models import {model_name}AppContentPlugin


@plugin_pool.register_plugin
class CMS{model_name}AppContentPlugin(CMSAllinkBaseAppContentPlugin):
    """
    model:
    - where to store plugin instances

    name:
    - name of the plugin
    """
    model = {model_name}AppContentPlugin
    name = model.data_model.get_verbose_name_plural()

'''

new_cms_toolbars = '''# -*- coding: utf-8 -*-
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.core.cms_toolbars import AllinkBaseModifierMixin

from {app_package}.models import {model_name}


class {model_name}Toolbar(AllinkBaseModifierMixin, CMSToolbar):
    model = {model_name}
    app_label = {model_name}._meta.app_label


toolbar_pool.register({model_name}Toolbar)

'''

new_config = '''# -*- coding: utf-8 -*-
from django.apps import AppConfig


class {model_name}Config(AppConfig):
    name = '{app_package}'
    verbose_name = "{model_name}"

'''

new_forms = '''# -*- coding: utf-8 -*-
'''

new_models = '''# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

from cms.models.fields import PageField
from cms.models.pluginmodel import CMSPlugin
from cms.models.fields import PlaceholderField
from adminsortable.models import SortableMixin
from parler.models import TranslatableModel, TranslatedField
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

from aldryn_translation_tools.models import TranslationHelperMixin
from aldryn_common.admin_fields.sortedm2m import SortedM2MModelField
from allink_core.core.models.models import AllinkBaseAppContentPlugin, AllinkBaseModel, AllinkBaseTranslatedFieldsModel
from allink_core.core.models.mixins import AllinkTranslatedAutoSlugifyMixin
from allink_core.core.models.managers import AllinkBaseModelManager


class {model_name}(SortableMixin, TranslationHelperMixin, AllinkTranslatedAutoSlugifyMixin, TranslatableModel, AllinkBaseModel):
    slug_source_field_name = 'title'

    title = TranslatedField(any_language=True)
    slug = TranslatedField(any_language=True)
    lead = TranslatedField()

    preview_image = FilerImageField(
        verbose_name=_(u'Preview Image'),
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_preview_image',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True
    )

    header_placeholder = PlaceholderField(u'{label}_header', related_name='%(app_label)s_%(class)s_header_placeholder')
    content_placeholder = PlaceholderField(u'{label}_content', related_name='%(app_label)s_%(class)s_content_placeholder')
    content_additional_placeholder = PlaceholderField(u'{label}_content_additional', related_name='%(app_label)s_%(class)s_content_additional_placeholder')

    objects = AllinkBaseModelManager()

    class Meta:
        app_label = '{label}'
        ordering = ('sort_order',)
        verbose_name = _('{model_name}')
        verbose_name_plural = _('{model_name}')


class {model_name}Translation(AllinkBaseTranslatedFieldsModel):
    master = models.ForeignKey('{label}.{model_name}', related_name='translations', null=True)

    title = models.CharField(
        max_length=255
    )
    slug = models.SlugField(
        _(u'Slug'),
        max_length=255,
        default='',
        blank=True,
        help_text=_(u'Leave blank to auto-generate a unique slug.')
    )
    lead = HTMLField(
        _(u'Lead Text'),
        help_text=_(u'Teaser text that in some cases is used in the list view and/or in the detail view.'),
        blank=True,
        null=True,
    )
    class Meta:
        app_label = '{label}'


class {model_name}AppContentPlugin(AllinkBaseAppContentPlugin):
    data_model = {model_name}

    manual_entries = SortedM2MModelField(
        '{label}.{model_name}',
        blank=True,
        help_text=_('Select and arrange specific entries, or, leave blank to select all. (If '
                    'manual entries are selected the category filtering will be ignored.)')
    )
    apphook_page = PageField(
        verbose_name=_(u'Apphook Page'),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text=_(u'If provided, this Apphook-Page will be used to generate the detail link.'),
    )

    def save(self, *args, **kwargs):
        # invalidate cache
        # cache.delete_many([make_template_fragment_key('{label}_preview_image', [self.id, {label}.id]) for {label} in {model_name}.objects.all()])
        super({model_name}AppContentPlugin, self).save(*args, **kwargs)

    class Meta:
        app_label = '{label}'

'''

new_sitemaps = '''# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap

from {app_package}.models import {model_name}


class {model_name}Sitemap(Sitemap):

    changefreq = "never"
    priority = 0.5
    i18n = True

    def __init__(self, *args, **kwargs):
        self.namespace = kwargs.pop('namespace', None)
        super({model_name}Sitemap, self).__init__(*args, **kwargs)

    def items(self):
        return {model_name}.objects.active()

    def lastmod(self, obj):
        return obj.modified

'''

new_urls = '''# # -*- coding: utf-8 -*-
from django.conf.urls import url

from {app_package}.views import {model_name}PluginLoadMore, {model_name}Detail


urlpatterns = [
    url(r'^(?P<page>[0-9]*)/$', {model_name}PluginLoadMore.as_view(), name='more'),
    url(r'^(?P<slug>[\w-]+)/$', {model_name}Detail.as_view(), name='detail'),
]

'''

new_views = '''# -*- coding: utf-8 -*-
from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView, AllinkBaseAjaxFormView

from {app_package}.models import {model_name}, {model_name}AppContentPlugin


class {model_name}PluginLoadMore(AllinkBasePluginLoadMoreView):
    model = {model_name}
    plugin_model = {model_name}AppContentPlugin


class {model_name}Detail(AllinkBaseDetailView):
    model = {model_name}

'''

def new_app(label, folder_path, logger=None):
    """
    Create a new app with all the basic functionality a allink app has.
    """

    if logger is None:
        logger = logging.getLogger(__name__)

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
    model_name = label.title().replace('_', '')

    # Create all snippets
    snippet_admin = new_admin.format(label=label, app_package=app_package, model_name=model_name)
    snippet_cms_apps = new_cms_apps.format(label=label, app_package=app_package, model_name=model_name)
    snippet_cms_menu = new_cms_menu.format(label=label, app_package=app_package, model_name=model_name)
    snippet_cms_plugins = new_cms_plugins.format(label=label, app_package=app_package, model_name=model_name)
    snippet_cms_toolbars = new_cms_toolbars.format(label=label, app_package=app_package, model_name=model_name)
    snippet_config = new_config.format(label=label, app_package=app_package, model_name=model_name)
    snippet_forms = new_forms.format(label=label, app_package=app_package, model_name=model_name)
    snippet_models = new_models.format(label=label, app_package=app_package, model_name=model_name)
    snippet_sitemaps = new_sitemaps.format(label=label, app_package=app_package, model_name=model_name)
    snippet_urls = new_urls.format(label=label, app_package=app_package, model_name=model_name)
    snippet_views = new_views.format(label=label, app_package=app_package, model_name=model_name)

    logger.info("Creating admin.py")
    create_file(join(local_app_path, 'admin.py'), snippet_admin)

    logger.info("Creating cms_apps.py")
    create_file(join(local_app_path, 'cms_apps.py'), snippet_cms_apps)

    logger.info("Creating cms_menu.py")
    create_file(join(local_app_path, 'cms_menu.py'), snippet_cms_menu)

    logger.info("Creating cms_plugins.py")
    create_file(join(local_app_path, 'cms_plugins.py'), snippet_cms_plugins)

    logger.info("Creating cms_toolbars.py")
    create_file(join(local_app_path, 'cms_toolbars.py'), snippet_cms_toolbars)

    logger.info("Creating config.py")
    create_file(join(local_app_path, 'config.py'), snippet_config)

    logger.info("Creating forms.py")
    create_file(join(local_app_path, 'forms.py'), snippet_forms)

    logger.info("Creating models.py")
    create_file(join(local_app_path, 'models.py'), snippet_models)

    logger.info("Creating sitemaps.py")
    create_file(join(local_app_path, 'sitemaps.py'), snippet_sitemaps)

    logger.info("Creating urls.py")
    create_file(join(local_app_path, 'urls.py'), snippet_urls)

    logger.info("Creating views.py")
    create_file(join(local_app_path, 'views.py'), snippet_views)

    # Final step needs to be done by hand
    msg = (
        "The final steps:\n"
        "1. add '{app_package}' to PROJECT_APPS \n"
        "2. add Plugins to CMS_ALLINK_CONTENT_PLUGIN_CHILD_CLASSES \n"
        "3. define templates/ create a new tuple {model_name_uppper}_PLUGIN_TEMPLATES \n"
        "4. (optional) add '('{model_name_lower}', '{model_name}'),' to PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES if the app should have categories \n"
        "5. create all required templates (default grid_static, detail and no_result)"
        "6. ./manage.py makemigrations {label} ./manage.py migrate\n\n"
    ).format(model_name=model_name, model_name_uppper=str.upper(model_name), model_name_lower=str.lower(model_name), app_package=app_package, label=label)

    logger.info(msg)
