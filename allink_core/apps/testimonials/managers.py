# -*- coding: utf-8 -*-
from allink_core.core.models.managers import AllinkCategoryModelQuerySet


class AllinkTestimonialsQuerySet(AllinkCategoryModelQuerySet):

    def title_asc(self):
        return self.active()\
            .order_by('first_name', 'id')\
            .distinct('first_name', 'id')

    def title_desc(self):
        return self.active()\
            .order_by('-first_name', 'id')\
            .distinct('first_name', 'id')

    def category(self):
        return self.active()\
            .order_by('categories__tree_id', 'categories__lft', 'first_name')\
            .distinct()


AllinkTestimonialsManager = AllinkTestimonialsQuerySet.as_manager
