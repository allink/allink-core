# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from cms.toolbar.items import Break
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMIN_SITES_BREAK
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.extensions.toolbar import ExtensionToolbar
from cms.utils import get_language_list

from allink_core.core.loading import get_model

Config = get_model('config', 'Config')

AllinkPageExtension = get_model('config', 'AllinkPageExtension')
AllinkTitleExtension = get_model('config', 'AllinkTitleExtension')


@toolbar_pool.register
class ConfigToolbar(CMSToolbar):
    model = Config

    def populate(self):
        admin_menu = self.toolbar.get_menu(ADMIN_MENU_IDENTIFIER)
        position = admin_menu.find_first(Break, identifier=ADMIN_SITES_BREAK)
        allink_menu = admin_menu.get_or_create_menu(
            'allink-menu',
            _('allink'),
            position=position
        )
        url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
        allink_menu.add_sideframe_item(_(u'Config'), url=url)


class AllinkPageExtensionToolbar(ExtensionToolbar):
    model = AllinkPageExtension

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()

        if current_page_menu and self.toolbar.edit_mode:
            page_extension, url = self.get_page_extension_admin()
            if url:
                current_page_menu.add_modal_item(_(u'allink settings'), url=url,
                    disabled=not self.toolbar.edit_mode, position=5)


toolbar_pool.register(AllinkPageExtensionToolbar)


class AllinkTitleExtensionToolbar(ExtensionToolbar):
    submenu_label = 'Translated page addition'
    model = AllinkTitleExtension

    """ action is used for additional naming on submenu node
        gets pulled from Model to make overriding easier
    """
    try:
        action = model.action
    except AttributeError:
        action = ''

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()

        if current_page_menu and self.toolbar.edit_mode:
            # create a sub menu labelled self.submenu_label in the menu
            sub_menu = self._get_sub_menu(
                current_page_menu, 'AllinkTitleExtensionToolbar', self.submenu_label, position=6
            )

            urls = self.get_title_extension_admin()

            # we now also need to get the titleset (i.e. different language titles)
            # for this page
            page = self._get_page()
            titleset = page.title_set.filter(language__in=get_language_list(page.site_id))

            # create a 3-tuple of (title_extension, url, title)
            nodes = [(title_extension, url, title.title) for (
                (title_extension, url), title) in zip(urls, titleset)
                     ]

            # cycle through the list of nodes
            for title_extension, url, title in nodes:
                # adds toolbar items
                sub_menu.add_modal_item(
                    '%s %s' % (self.action, title), url=url, disabled=not self.toolbar.edit_mode
                )

if getattr(Config.get_solo(), 'config_allink_title_toolbar_enabled', True):
    toolbar_pool.register(AllinkTitleExtensionToolbar)
