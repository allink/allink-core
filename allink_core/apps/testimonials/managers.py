# -*- coding: utf-8 -*-
from allink_core.core.models.managers import AllinkBaseModelQuerySet, AllinkBaseModelManager


class AllinkTestimonialQuerySet(AllinkBaseModelQuerySet):

    def title_asc(self):
        return self.active_entries()\
            .order_by('first_name', 'id')\
            .distinct('first_name', 'id')

    def title_desc(self):
        return self.active_entries()\
            .order_by('-first_name', 'id')\
            .distinct('first_name', 'id')

    def category(self):
        return self.active_entries()\
            .order_by('categories__tree_id', 'categories__lft', 'first_name')\
            .distinct()


class AllinkTestimonialManager(AllinkBaseModelManager):
    queryset_class = AllinkTestimonialQuerySet
