# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from cms.toolbar.items import Break
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMIN_SITES_BREAK
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.extensions.toolbar import ExtensionToolbar

from allink_core.allink_config.models import AllinkMetaTagExtension, AllinkConfig


@toolbar_pool.register
class AllinkMetaTagExtensionToolbar(ExtensionToolbar):
    model = AllinkMetaTagExtension

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()
        if current_page_menu and self.toolbar.edit_mode:
            position = 5
            sub_menu = self._get_sub_menu(current_page_menu, 'submenu_label', _(u'Meta Tags'), position)
            urls = self.get_title_extension_admin()

            for title_extension, url in urls:
                sub_menu.add_modal_item(_(u'{}').format(self._get_page().get_title()), url=url, disabled=not self.toolbar.edit_mode)


@toolbar_pool.register
class AllinkConfigToolbar(CMSToolbar):
    model = AllinkConfig

    def populate(self):
        admin_menu = self.toolbar.get_menu(ADMIN_MENU_IDENTIFIER)
        position = admin_menu.find_first(Break, identifier=ADMIN_SITES_BREAK)
        allink_menu = admin_menu.get_or_create_menu(
            'allink-menu',
            _('Allink'),
            position=position
        )

        url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
        allink_menu.add_sideframe_item(_(u'Config'), url=url)
