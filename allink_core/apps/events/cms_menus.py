# -*- coding: utf-8 -*-
from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _
from cms.menu_bases import CMSAttachMenu

from allink_core.core.loading import get_model, get_class


Events= get_model('events', 'Events')


class EventsMenu(CMSAttachMenu):

    name = _("Events menu")

    def get_nodes(self, request):

        nodes = []
        for entry in Events.objects.active():
            node = NavigationNode(
                entry.title,
                entry.get_absolute_url(),
                attr={
                    'description': entry.lead
                })
            nodes.append(node)

        return nodes


menu_pool.register_menu(get_class('events.cms_menus', 'EventsMenu'))
