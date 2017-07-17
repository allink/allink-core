# -*- coding: utf-8 -*-
from datetime import datetime
from django.db.models import Q
from allink_core.core.models.managers import AllinkBaseModelQuerySet, AllinkBaseModelManager


class AllinkEventsQuerySet(AllinkBaseModelQuerySet):
    def active_entries(self):
        today = datetime.today()
        return self.active_translations()\
            .filter(Q(is_active=True) & (Q(start__isnull=True) & Q(end__isnull=True)) | ((Q(start__lte=today) & Q(end__isnull=True)) | (Q(start__isnull=True) & Q(end__gte=today))) | (Q(start__lte=today) & Q(end__gte=today)))

    def latest(self):
        return self.active_entries()\
            .order_by('event_date_time', 'id')\
            .distinct('event_date_time', 'id')

    def earliest(self):
        return self.active_entries()\
            .order_by('-event_date_time', 'id')\
            .distinct('event_date_time', 'id')

    def category(self):
        return self.active_entries()\
            .order_by('categories__tree_id', 'categories__lft', 'event_date_time')\
            .distinct()


class AllinkEventsManager(AllinkBaseModelManager):
    queryset_class = AllinkEventsQuerySet
