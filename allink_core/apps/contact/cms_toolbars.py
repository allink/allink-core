# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth import get_permission_codename

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.core.loading import get_model


Config = get_model('config', 'Config')
ContactRequest = get_model('contact', 'ContactRequest')


class ContactToolbar(CMSToolbar):
    model = ContactRequest

    def populate(self):
        opts = self.model._meta

        if self.request.user.has_perm('%s.%s' % (opts.app_label, get_permission_codename('change', opts))):
            menu = self.toolbar.get_or_create_menu('form-menu', _('Forms'))
            url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
            menu.add_sideframe_item(self.model.get_verbose_name_plural(), url=url)


toolbar_pool.register(ContactToolbar)
