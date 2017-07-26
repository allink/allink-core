# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from cms.toolbar.items import Break
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMIN_SITES_BREAK
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.extensions.toolbar import ExtensionToolbar

from allink_core.core.loading import get_model

Config = get_model('config', 'Config')
AllinkPageExtension = get_model('config', 'AllinkPageExtension')


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

if getattr(Config.get_solo(), 'config_allink_page_toolbar_enabled', True):
    toolbar_pool.register(AllinkPageExtensionToolbar)
