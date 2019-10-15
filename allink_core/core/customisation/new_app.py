# -*- coding: utf-8 -*-
import logging
from os.path import join
from .utils import create_local_app_folder, create_file

new_admin = '''# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from adminsortable.admin import SortableAdmin
from cms.admin.placeholderadmin import PlaceholderAdminMixin
from parler.admin import TranslatableAdmin
from allink_core.core.admin import AllinkMediaAdminMixin, AllinkSEOAdminMixin, AllinkCategoryAdminMixin, AllinkTeaserAdminMixin

from .models import {model_name}


@admin.register({model_name})
class {model_name}Admin(AllinkMediaAdminMixin, AllinkSEOAdminMixin, AllinkCategoryAdminMixin, AllinkTeaserAdminMixin, 
                        PlaceholderAdminMixin, TranslatableAdmin, SortableAdmin):
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
                )
            }}),
        )

        fieldsets += self.get_category_fieldsets()
        fieldsets += self.get_teaser_fieldsets()
        fieldsets += self.get_seo_fieldsets()
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

new_cms_plugins = '''# -*- coding: utf-8 -*-
from cms.plugin_pool import plugin_pool
from allink_core.core.cms_plugins import CMSAllinkBaseAppContentPlugin

from .models import {model_name}AppContentPlugin


@plugin_pool.register_plugin
class CMS{model_name}AppContentPlugin(CMSAllinkBaseAppContentPlugin):
    """
    model:
    - where to store plugin instances

    name:
    - name of the plugin
    """
    model = {model_name}AppContentPlugin
    name = model.data_model._meta.verbose_name_plural

'''

new_cms_toolbars = '''# -*- coding: utf-8 -*-
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.core.cms_toolbars import AllinkBaseModifierMixin
from .models import {model_name}


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

new_models = '''# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models

from cms.models.fields import PageField
from cms.models.fields import PlaceholderField
from adminsortable.models import SortableMixin
from parler.models import TranslatedField
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

from aldryn_common.admin_fields.sortedm2m import SortedM2MModelField
from allink_core.core.models import (
    AllinkCategoryFieldsModel,
    AllinkBaseTranslatableModel,
    AllinkBaseAppContentPlugin,
    AllinkBaseTranslatedFieldsModel,
)
from .managers import {model_name}Manager()


class {model_name}(SortableMixin, AllinkCategoryFieldsModel, AllinkBaseTranslatableModel):
    slug_source_field_name = 'title'

    title = TranslatedField(any_language=True)
    lead = TranslatedField()

    preview_image = FilerImageField(
        verbose_name='Preview Image',
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name='%(app_label)s_%(class)s_preview_image',
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        editable=False,
        db_index=True
    )

    header_placeholder = PlaceholderField(
       '{label}_header',
        related_name='%(app_label)s_%(class)s_header_placeholder'
    )
    
    content_placeholder = PlaceholderField(
       '{label}_content',
        related_name='%(app_label)s_%(class)s_content_placeholder'
    )

    objects = Allink{model_name}Manager()

    class Meta:
        app_label = '{label}'
        ordering = ('sort_order',)
        verbose_name = '{model_name}'
        verbose_name_plural = '{model_name}'


class {model_name}Translation(AllinkBaseTranslatedFieldsModel):
    master = models.ForeignKey(
        '{label}.{model_name}',
        on_delete=models.CASCADE,
        related_name='translations',
        null=True
        )

    title = models.CharField(
        max_length=255
    )
    lead = HTMLField(
        _('Lead Text'),
        help_text='Teaser text that in some cases is used in the list view and/or in the detail view.',
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
        help_text=('Select and arrange specific entries, or, leave blank to select all. (If '
                    'manual entries are selected the category filtering will be applied as well.)')
    )
    apphook_page = PageField(
        verbose_name='Apphook Page',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text='If provided, this Apphook-Page will be used to generate the detail link.',
    )

    class Meta:
        app_label = '{label}'

'''

new_managers = '''# -*- coding: utf-8 -*-
from allink_core.core.models.managers import AllinkCategoryModelQuerySet


class {model_name}QuerySet(AllinkCategoryModelQuerySet):
    pass


{model_name}Manager = {model_name}QuerySet.as_manager

'''

new_sitemaps = '''# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap
from .models import {model_name}


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
from django.urls import path
from .views import {model_name}PluginLoadMore, {model_name}Detail


urlpatterns = [
    path('<int:page>/', {model_name}PluginLoadMore.as_view(), name='more'),
    path('<slug:slug>/', {model_name}Detail.as_view(), name='detail'),
]

'''

new_views = '''# -*- coding: utf-8 -*-
from allink_core.core.views import AllinkBasePluginLoadMoreView, AllinkBaseDetailView

from .models import {model_name}, {model_name}AppContentPlugin


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
    snippet_cms_plugins = new_cms_plugins.format(label=label, app_package=app_package, model_name=model_name)
    snippet_cms_toolbars = new_cms_toolbars.format(label=label, app_package=app_package, model_name=model_name)
    snippet_config = new_config.format(label=label, app_package=app_package, model_name=model_name)
    snippet_models = new_models.format(label=label, app_package=app_package, model_name=model_name)
    snippet_managers = new_managers.format(label=label, app_package=app_package, model_name=model_name)
    snippet_sitemaps = new_sitemaps.format(label=label, app_package=app_package, model_name=model_name)
    snippet_urls = new_urls.format(label=label, app_package=app_package, model_name=model_name)
    snippet_views = new_views.format(label=label, app_package=app_package, model_name=model_name)

    logger.info("Creating admin.py")
    create_file(join(local_app_path, 'admin.py'), snippet_admin)

    logger.info("Creating cms_apps.py")
    create_file(join(local_app_path, 'cms_apps.py'), snippet_cms_apps)

    logger.info("Creating cms_plugins.py")
    create_file(join(local_app_path, 'cms_plugins.py'), snippet_cms_plugins)

    logger.info("Creating cms_toolbars.py")
    create_file(join(local_app_path, 'cms_toolbars.py'), snippet_cms_toolbars)

    logger.info("Creating config.py")
    create_file(join(local_app_path, 'config.py'), snippet_config)

    logger.info("Creating models.py")
    create_file(join(local_app_path, 'models.py'), snippet_models)

    logger.info("Creating managers.py")
    create_file(join(local_app_path, 'managers.py'), snippet_managers)

    logger.info("Creating sitemaps.py")
    create_file(join(local_app_path, 'sitemaps.py'), snippet_sitemaps)

    logger.info("Creating urls.py")
    create_file(join(local_app_path, 'urls.py'), snippet_urls)

    logger.info("Creating views.py")
    create_file(join(local_app_path, 'views.py'), snippet_views)

    # Final step needs to be done by hand
    msg = (
        """
            The final steps:\n
            1. add '{app_package}' to PROJECT_APPS \n
            2. add Plugins to ALLINK_CONTENT_PLUGIN_CHILD_CLASSES \n
            3. add '('{{model_name}}Apphook', {'detail': ('apps.{{app_package}}.models.{{model_name}}', ['slug'])}),' to PROJECT_LINK_APPHOOKS \n
            4. create a new tuple {model_name_upper}_PLUGIN_TEMPLATES and add all templates from templates/ dir \n
            5. (optional) add '('{model_name_lower}', '{model_name}'),' to PROJECT_APP_MODEL_WITH_CATEGORY_CHOICES if the app should have categories \n
            6. ./manage.py makemigrations {label} ./manage.py migrate\n\n
        """
    ).format(
        model_name=model_name,
        model_name_upper=str.upper(model_name),
        model_name_lower=str.lower(model_name),
        app_package=app_package,
        label=label
    )

    logger.info(msg)
