# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


class AllinkBaseModifierMixin(object):
    """
    BaseModifierMixin for basic Toolbar
    Just override model = None to specific model

    # model = <<modelclass>>
    """

    model = None

    def populate(self):

        apps_menu = self.toolbar.get_or_create_menu(
            'apps-menu'.format(self.model._meta.model_name),
            _('Apps')
        )

        menu = apps_menu.get_or_create_menu(
            '{}-menu'.format(self.model._meta.model_name),
            _('{}'.format(self.model.get_verbose_name_plural()))
        )

        url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
        menu.add_sideframe_item(_('{} List'.format(self.model.get_verbose_name_plural())), url=url)

        url = reverse('admin:{}_{}_add'.format(self.model._meta.app_label, self.model._meta.model_name))
        menu.add_modal_item(_('Add new {}'.format(self.model.get_verbose_name())), url=url)

    def post_template_populate(self):
        pass

    def request_hook(self):
        pass
