# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.core_apps.allink_terms.models import AllinkTerms
from allink_core.core.loading import get_model

Config = get_model('config', 'Config')


class AllinkTermsToolbar(CMSToolbar):
    model = AllinkTerms

    def populate(self):
        menu = self.toolbar.get_or_create_menu(
            '{}-menu'.format(self.model._meta.model_name),
            _('{}'.format(self.model._meta.verbose_name_plural))
        )
        url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
        menu.add_sideframe_item(self.model._meta.verbose_name_plural, url=url)


toolbar_pool.register(AllinkTermsToolbar)
