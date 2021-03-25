# -*- coding: utf-8 -*-
from parler.managers import TranslatableQuerySet


class AllinkBaseModelQuerySet(TranslatableQuerySet):

    def active(self):
        return self.filter(status=1)

    def filter_by_categories(self, categories):
        return self.active() \
            .filter(categories__in=categories) \
            .distinct()

    def filter_by_category(self, category):
        return self.active() \
            .filter(categories=category) \
            .distinct()

    # ORDERING
    def latest(self):
        return self.active() \
            .order_by('-created', 'id') \
            .distinct('created', 'id')

    def earliest(self):
        return self.active() \
            .order_by('created', 'id').distinct('created', 'id')

    # A-Z
    def title_asc(self, lang):
        return self.active() \
            .translated(lang) \
            .order_by('translations__title')

    # Z-A
    def title_desc(self, lang):
        return self.active() \
            .translated(lang) \
            .order_by('-translations__title')


AllinkBaseModelManager = AllinkBaseModelQuerySet.as_manager


class AllinkCategoryModelQuerySet(AllinkBaseModelQuerySet):

    def category(self):
        return self.active() \
            .order_by('categories__tree_id', 'categories__lft', 'translations__title') \
            .distinct()


AllinkCategoryModelManager = AllinkCategoryModelQuerySet.as_manager
