# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language
from cms.toolbar_pool import toolbar_pool
from cms.utils import get_language_list
from cms.extensions.toolbar import ExtensionToolbar

from allink_core.core_apps.allink_seo.models import AllinkSEOExtension


@toolbar_pool.register
class AllinkSEOExtensionToolbar(ExtensionToolbar):
    model = AllinkSEOExtension

    def populate(self):
        current_page_menu = self._setup_extension_toolbar()
        if current_page_menu and self.toolbar.edit_mode:

            sub_menu = self._get_sub_menu(current_page_menu, 'submenu_label', _(u'SEO'), position=5)
            languages = get_language_list(self._get_page().site_id)

            for language in languages:
                extensions = self.get_title_extension_admin(language=language)
                sub_menu.add_modal_item(_(u'{}').format(language), url=extensions[0][1], disabled=not self.toolbar.edit_mode)

