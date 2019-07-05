# -*- coding: utf-8 -*-
from datetime import datetime
from django.db.models import Q
from allink_core.core.models.managers import AllinkCategoryModelQuerySet


class AllinkEventsQuerySet(AllinkCategoryModelQuerySet):
    def active(self):
        today = datetime.today()
        return self.filter(
            Q(status=1)
            & (Q(start__isnull=True) & Q(end__isnull=True))
            | ((Q(start__lte=today) & Q(end__isnull=True))
               | (Q(start__isnull=True) & Q(end__gte=today)))
            | (Q(start__lte=today) & Q(end__gte=today)))

    def latest(self):
        return self.active()\
            .order_by('entry_date', 'id')\
            .distinct('entry_date', 'id')

    def earliest(self):
        return self.active()\
            .order_by('-entry_date', 'id')\
            .distinct('entry_date', 'id')

    def category(self):
        return self.active()\
            .order_by('categories__tree_id', 'categories__lft', 'entry_date')\
            .distinct()

    def upcoming_entries(self):
        today = datetime.today()
        return self.filter(entry_date__gte=today)

    def past_entries(self):
        today = datetime.today()
        return self.filter(entry_date__lte=today)


AllinkEventsManager = AllinkEventsQuerySet.as_manager
