# -*- coding: utf-8 -*-
from django.urls import reverse
from django.contrib.auth import get_permission_codename


class AllinkBaseModifierMixin:
    """
    BaseModifierMixin for basic Toolbar
    Just override model = None to specific model

    # model = <<modelclass>>
    """

    model = None

    def populate(self):
        opts = self.model._meta
        permissions_added = 0

        apps_menu = self.toolbar.get_or_create_menu(
            'apps-menu'.format(self.model._meta.model_name),
            'Apps'
        )

        menu = apps_menu.get_or_create_menu(
            '{}-menu'.format(self.model._meta.model_name),
            '{}'.format(self.model._meta.verbose_name_plural)
        )

        if self.request.user.has_perm('%s.%s' % (opts.app_label, get_permission_codename('change', opts))):
            permissions_added += 1
            url = reverse('admin:{}_{}_changelist'.format(self.model._meta.app_label, self.model._meta.model_name))
            menu.add_sideframe_item('{} List'.format(self.model._meta.verbose_name_plural), url=url)

        if self.request.user.has_perm('%s.%s' % (opts.app_label, get_permission_codename('add', opts))):
            permissions_added += 1
            url = reverse('admin:{}_{}_add'.format(self.model._meta.app_label, self.model._meta.model_name))
            menu.add_modal_item('Add new {}'.format(self.model._meta.verbose_name), url=url)

        menu, opts, permissions_added = self.custom_permissions(menu, opts, permissions_added)

        if permissions_added == 0:
            menu.disabled = True

    def custom_permissions(self, menu, opts, permissions_added):
        return menu, opts, permissions_added

    def post_template_populate(self):
        pass

    def request_hook(self):
        pass
