# -*- coding: utf-8 -*-
from datetime import datetime
from django.db.models import Q
from allink_core.core.models.managers import AllinkBaseModelQuerySet, AllinkBaseModelManager


class AllinkEventsQuerySet(AllinkBaseModelQuerySet):
    def active_entries(self):
        today = datetime.today()
        return self.filter(Q(status=1) & (Q(start__isnull=True) & Q(end__isnull=True)) | ((Q(start__lte=today) & Q(end__isnull=True)) | (Q(start__isnull=True) & Q(end__gte=today))) | (Q(start__lte=today) & Q(end__gte=today)))

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

    def upcoming_entries(self):
        today = datetime.today()
        return self.filter(event_date_time__gte=today)

    def past_entries(self):
        today = datetime.today()
        return self.filter(event_date_time__lte=today)


class AllinkEventsManager(AllinkBaseModelManager):
    queryset_class = AllinkEventsQuerySet
