# -*- coding: utf-8 -*-
from django.conf import settings
from menus.menu_pool import menu_pool
from menus.base import Modifier
from cms.models import Page
from allink_core.core.loading import get_class


class AllinkPageMenuModifier(Modifier):

    def modify(self, request, nodes, namespace, root_id, post_cut, breadcrumb):
        # only do something when the menu has already been cut
        if post_cut:
            # only consider nodes that refer to cms pages
            # and put them in a dict for efficient access
            page_nodes = {n.id: n for n in nodes if n.attr["is_page"]}
            # retrieve the attributes of interest from the relevant pages
            pages = Page.objects.filter(id__in=page_nodes.keys(),
                                        allinkpageextension__isnull=False).values('id', 'allinkpageextension')
            # loop over all relevant pages
            for page in pages:
                # take the node referring to the page
                node = page_nodes[page['id']]
                # put the changed_by attribute on the node
                node.attr["special_nav"] = page['allinkpageextension']
        return nodes


if getattr(settings, 'ALLINK_PAGE_TOOLBAR_ENABLED', False):
    menu_pool.register_modifier(get_class('config.cms_menus', 'AllinkPageMenuModifier'))
