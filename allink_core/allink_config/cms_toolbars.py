# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.extensions.toolbar import ExtensionToolbar

from .models import AllinkMetaTagExtension


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
