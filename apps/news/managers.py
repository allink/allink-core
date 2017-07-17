# -*- coding: utf-8 -*-
from datetime import datetime
from django.db.models import Q
from allink_core.core.models.managers import AllinkBaseModelQuerySet, AllinkBaseModelManager


class AllinkNewsQuerySet(AllinkBaseModelQuerySet):
    def active_entries(self):
        today = datetime.today()
        return self.active_translations()\
            .filter(Q(is_active=True) & (Q(start__isnull=True) & Q(end__isnull=True)) | ((Q(start__lte=today) & Q(end__isnull=True)) | (Q(start__isnull=True) & Q(end__gte=today))) | (Q(start__lte=today) & Q(end__gte=today)))


class AllinkNewsManager(AllinkBaseModelManager):
    queryset_class = AllinkNewsQuerySet
