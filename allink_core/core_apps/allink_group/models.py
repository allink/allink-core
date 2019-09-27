# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from cms.models.pluginmodel import CMSPlugin


class AllinkGroupContainerPlugin(CMSPlugin):
    """
    A Container-Plugin for Group of Content
    """

    title = models.CharField(
        _('Title'),
        max_length=255
    )

    groups = models.ManyToManyField(
        Group,
        blank=True,
    )

    def __str__(self):
        return self.title

    def copy_relations(self, oldinstance):
        for i in oldinstance.groups.all():
            self.groups.add(i)


class AllinkGroupPlugin(CMSPlugin):
    title = models.CharField(
        _('Title'),
        max_length=255
    )

    def __str__(self):
        return '{}'.format(self.title)
