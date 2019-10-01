# -*- coding: utf-8 -*-
from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from cms.menu_bases import CMSAttachMenu

from allink_core.core.loading import get_model, get_class


News = get_model('news', 'News')


class NewsMenu(CMSAttachMenu):

    name = "News menu"

    def get_nodes(self, request):

        nodes = []
        for entry in News.objects.active():
            node = NavigationNode(
                entry.title,
                entry.get_absolute_url(),
                attr={
                    'description': entry.lead
                })
            nodes.append(node)

        return nodes


menu_pool.register_menu(get_class('news.cms_menus', 'NewsMenu'))
