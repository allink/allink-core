# -*- coding: utf-8 -*-

from allink_core.core.models.managers import AllinkBaseModelQuerySet, AllinkBaseModelManager


class AllinkPeopleQuerySet(AllinkBaseModelQuerySet):

    def title_asc(self):
        return self.active_entries()\
            .order_by('last_name', 'id')\
            .distinct('last_name', 'id')

    def title_desc(self):
        return self.active_entries()\
            .order_by('-last_name', 'id')\
            .distinct('last_name', 'id')

    def category(self):
        return self.active_entries()\
            .order_by('categories__tree_id', 'categories__lft', 'last_name')\
            .distinct()


class AllinkPeopleManager(AllinkBaseModelManager):
    queryset_class = AllinkPeopleQuerySet
    use_for_related_fields = True
