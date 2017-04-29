# -*- coding: utf-8 -*-
from parler.managers import TranslatableManager, TranslatableQuerySet


class AllinkBaseModelQuerySet(TranslatableQuerySet):

    def active_entries(self):
        ''' entries which are active
        '''
        return self.translated()\
            .filter(is_active=True)

    def filter_by_categories(self, categories):
        ''' entries with categories
            in categories
        '''
        return self.active_entries()\
            .filter(categories__in=categories)

    def filter_by_category(self, category):
        return self.active_entries()\
            .filter(categories=category)

    # ORDERING

    def latest(self):
        return self.active_entries()\
            .order_by('-created', 'id')\
            .distinct('created', 'id')

    def earliest(self):
        return self \
            .active_entries()\
            .order_by('created', 'id').distinct('created', 'id')

    def title_asc(self):
        # TODO
        # result = self.active_translations().order_by('translations__title', 'id').distinct('translations__title', 'id')
        # def remove_dublicates(seq):
        #     seen = set()
        #     seen_add = seen.add
        #     return [x for x in seq if not (x in seen or seen_add(x))]
        # return remove_dublicates(result)
        return self.active_entries()\
            .order_by('translations__title', 'id')\
            .distinct('translations__title', 'id')

    def title_desc(self):
        return self.active_entries()\
            .order_by('-translations__title', 'id')\
            .distinct('translations__title', 'id')

    def random(self):
        return self.active_entries()\
            .order_by('?')\
            .distinct()


class AllinkBaseModelManager(TranslatableManager):
    use_for_related_fields = True
    queryset_class = AllinkBaseModelQuerySet

    def active(self):
        q = self.get_queryset()\
            .active_entries()
        return q

    def filter_by_categories(self, categories):
        """
        :param categories:
        - relatedqueryset of AllinkCategories
        :return:
        - all instances where category is equal to one of the provided categories
        - only one entry per category
        - no ordering
        """
        q = self.get_queryset()\
            .active_entries()\
            .filter_by_categories(categories=categories.select_related())\
            .distinct()
        return q

    def filter_by_category(self, category):
        """
        :param categories:
        - relatedqueryset of AllinkCategories
        :return:
        - all instances where category is equal to one of the provided categories
        - only one entry per category
        - no ordering
        """
        q = self.get_queryset()\
            .active_entries() \
            .filter_by_category(category=category)\
            .distinct()
        return q
