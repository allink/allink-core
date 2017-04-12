# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.allink_terms.models import AllinkTerms
from allink_core.allink_config.models import AllinkConfig


class AllinkTermsToolbar(CMSToolbar):
    model = AllinkTerms

    def populate(self):
        menu = self.toolbar.get_or_create_menu(
            '{}-menu'.format(self.model._meta.model_name),
            _('{}'.format(self.model._meta.verbose_name_plural))
        )
        url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
        menu.add_sideframe_item(self.model._meta.verbose_name_plural, url=url)


if AllinkConfig.get_solo().terms_toolbar_enabled:
    toolbar_pool.register(AllinkTermsToolbar)
