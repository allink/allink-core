# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar

from allink_core.core.cms_toolbars import AllinkBaseModifierMixin
from allink_core.core.loading import get_model

Events = get_model('events', 'Events')
EventsRegistration = get_model('events', 'EventsRegistration')

Config = get_model('config', 'Config')
config = Config.get_solo()


class EventsToolbar(AllinkBaseModifierMixin, CMSToolbar):
    model = Events
    app_label = Events._meta.app_label


toolbar_pool.register(EventsToolbar)


class EventsRegistrationToolbar(CMSToolbar):
    model = EventsRegistration

    def populate(self):
        menu = self.toolbar.get_or_create_menu('form-menu', _('Forms'))

        url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
        menu.add_sideframe_item(self.model.get_verbose_name_plural(), url=url)

toolbar_pool.register(EventsRegistrationToolbar)
