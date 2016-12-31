# -*- coding: utf-8 -*-

import datetime
from django.db import models
from parler.managers import TranslatableManager, TranslatableQuerySet

class AllinkBaseModelQuerySet(TranslatableQuerySet):
    def active_entries(self):
        ''' entries which are active
        '''
        return self.filter(active=True)

    def filter_by_categories(self, categories):
        ''' entries with categories
            in categories
        '''
        return self.filter(categories__in=categories)

    def filter_by_category(self, category):
        return self.filter(categories=category)

    def latest(self):
        return self.order_by('-created', 'id').distinct('created', 'id')

    def oldest(self):
        return self.order_by('created', 'id').distinct('created', 'id')

    def title_asc(self):
        return self.order_by('translations__title', 'id').distinct('translations__lastname', 'id')

    def title_desc(self):
        return self.order_by('-translations__title', 'id').distinct('translations__lastname', 'id')


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
            .filter_by_categories(categories=categories.select_related().values_list('id'))\
            .distinct('id')
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
            .active_entries()\
            .filter_by_category(category=category)\
            .distinct('id')
        return q
