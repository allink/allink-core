# -*- coding: utf-8 -*-
from datetime import datetime
from django.db.models import Q
from allink_core.core.models.managers import AllinkBaseModelQuerySet


class AllinkNewsQuerySet(AllinkBaseModelQuerySet):
    def active(self):
        """
        :return:
        all entries which are active today
        """
        today = datetime.today()
        return self.published(start=today, end=today).filter(status=1)

    def latest(self):
        return self.active()\
            .order_by('-entry_date', 'id')\
            .distinct('entry_date', 'id')

    def earliest(self):
        return self.active()\
            .order_by('entry_date', 'id')\
            .distinct('entry_date', 'id')

    def published_fields_empty(self):
        return self.filter(Q(start__isnull=True) & Q(end__isnull=True))

    def published_with_startdate(self, start):
        return self.filter(Q(start__lte=start) & Q(end__isnull=True))

    def published_with_enddate(self, end):
        return self.filter(Q(start__isnull=True) & Q(end__gte=end))

    def published(self, start, end):
        return self.filter(Q(start__lte=start) & Q(end__gte=end)) | self.published_with_startdate(
            start) | self.published_with_enddate(end) | self.published_fields_empty()


AllinkNewsManager = AllinkNewsQuerySet.as_manager
