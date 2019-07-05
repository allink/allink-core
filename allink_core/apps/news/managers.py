# -*- coding: utf-8 -*-
from datetime import datetime
from django.db.models import Q
from allink_core.core.models.managers import AllinkBaseModelQuerySet


class AllinkNewsQuerySet(AllinkBaseModelQuerySet):
    def active(self):
        # return self.published_with_enddate().union(self.published_with_startdate().union(self.published_
        # with_daterange().union(self.datefields_empty().filter(status=1))))
        # return self.published_with_enddate().self.published_with_startdate().self.published_with_daterange(
        # ).self.datefields_empty().filter(status=1)

        return self.published_with_daterange() | self.published_with_startdate() | self.published_with_enddate() | self.datefields_empty().filter(status=1) #ist einiges performanter

    def datefields_empty(self):
        return self.filter(Q(start__isnull=True) & Q(end__isnull=True))

    def published_with_startdate(self):
        today = datetime.today()
        return self.filter(Q(start__lte=today) & Q(end__isnull=True))

    def published_with_enddate(self):
        today = datetime.today()
        return self.filter(Q(start__isnull=True) & Q(end__gte=today))

    def published_with_daterange(self):
        today = datetime.today()
        return self.filter(Q(start__lte=today) & Q(end__gte=today))


AllinkNewsManager = AllinkNewsQuerySet.as_manager

# def active(self):
#     today = datetime.today()
#     return self.published(today) | self.datefields_empty() | self.published_with_startdate(today) |
#     self.published_with_enddate(today)
# def datefields_empty(self):
#     return self.filter(Q(status=1)
#                        & (Q(start__isnull=True)
#                           & Q(end__isnull=True)))
#
# def published_with_startdate(self, today):
#     return self.filter(Q(start__lte=today) & Q(end__isnull=True))
#
# def published_with_enddate(self, today):
#     return self.filter(Q(start__isnull=True) & Q(end__gte=today))
#
# def published(self, today):
#     return self.filter(Q(start__lte=today) & Q(end__gte=today))


# News.objects.active().published(today=not_today)

# return self.filter(self.datefields_empty()
#                    & self.published_with_startdate(today)
#                    & self.published_with_enddate(today)
#                    & self.published(today))
# self.filter(Q(status=1)
# & (Q(start__isnull=True)
#    & Q(end__isnull=True)) | (
#     (Q(start__lte=today) & Q(end__isnull=True)) | (Q(start__isnull=True) & Q(end__gte=today))) | (
#     Q(start__lte=today) & Q(end__gte=today)))
