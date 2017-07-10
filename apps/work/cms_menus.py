# -*- coding: utf-8 -*-
from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _
from cms.menu_bases import CMSAttachMenu

from allink_core.core.loading import get_model, get_class


Work = get_model('work', 'Work')


class WorkMenu(CMSAttachMenu):

    name = _("Work menu")

    def get_nodes(self, request):

        nodes = []
        for entry in Work.objects.active():
            node = NavigationNode(
                entry.title,
                entry.get_absolute_url(),
                entry.sort_order,
                attr={
                    'description': entry.lead
                })
            nodes.append(node)

        return nodes


menu_pool.register_menu(get_class('work.cms_menus', 'WorkMenu'))
