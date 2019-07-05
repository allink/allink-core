# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from cms.toolbar.items import Break
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMIN_SITES_BREAK
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.extensions.toolbar import ExtensionToolbar

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
            'allink',
            position=position
        )
        url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
        allink_menu.add_sideframe_item(_('Config'), url=url)


class AllinkPageExtensionToolbar(ExtensionToolbar):
    model = AllinkPageExtension

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()
        if current_page_menu and self.toolbar.edit_mode_active:
            position = 5
            sub_menu = self._get_sub_menu(current_page_menu, 'submenu_label', 'Meta settings', position)
            urls = self.get_title_extension_admin()
            for title_extension, url in urls:
                sub_menu.add_modal_item('Images', url=url,
                                        disabled=not self.toolbar.edit_mode_active)


toolbar_pool.register(AllinkPageExtensionToolbar)


class AllinkTitleExtensionToolbar(ExtensionToolbar):
    model = AllinkTitleExtension

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()
        if current_page_menu and self.toolbar.edit_mode_active:
            position = 5
            sub_menu = self._get_sub_menu(current_page_menu, 'submenu_label', 'Meta settings', position)
            urls = self.get_title_extension_admin()
            for title_extension, url in urls:
                # adds toolbar items
                sub_menu.add_modal_item('Text', url=url,
                                        disabled=not self.toolbar.edit_mode_active)


toolbar_pool.register(AllinkTitleExtensionToolbar)
