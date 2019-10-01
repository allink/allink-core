# -*- coding: utf-8 -*-
from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

from allink_core.core.loading import get_model, get_class


People = get_model('people', 'People')


class PeopleMenu(CMSAttachMenu):

    name = "People menu"

    def get_nodes(self, request):

        nodes = []
        for entry in People.objects.active():
            node = NavigationNode(
                entry.title,
                entry.get_absolute_url(),
                entry.sort_order,
                attr={
                    'description': entry.lead
                })
            nodes.append(node)

        return nodes


menu_pool.register_menu(get_class('people.cms_menus', 'PeopleMenu'))
