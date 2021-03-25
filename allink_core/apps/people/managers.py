# -*- coding: utf-8 -*-

from allink_core.core.models.managers import AllinkCategoryModelQuerySet


class AllinkPeopleQuerySet(AllinkCategoryModelQuerySet):

    def title_asc(self, lang):
        return self.active()\
            .order_by('last_name', 'id')\
            .distinct('last_name', 'id')

    def title_desc(self, lang):
        return self.active()\
            .order_by('-last_name', 'id')\
            .distinct('last_name', 'id')

    def category(self):
        return self.active()\
            .order_by('categories__tree_id', 'categories__lft', 'last_name')\
            .distinct()


AllinkPeopleManager = AllinkPeopleQuerySet.as_manager
